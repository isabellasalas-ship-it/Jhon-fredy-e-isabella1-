import tkinter as tk
from tkinter import ttk, messagebox

import tema
from cliente_api import ErrorAPI

STOCK_BAJO = 5


def formato_precio(valor):
    numero = float(valor)
    if numero.is_integer():
        return f"${numero:,.0f}"
    return f"${numero:,.2f}"


class PestanaProductos(ttk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, style="Marco.TFrame")
        self.app = app
        self.productos = []
        self.id_seleccionado = None
        self.botones = []

        self._crear_formulario()
        self._crear_barra_busqueda()
        self._crear_tabla()

    # ---------- Construcción de la interfaz ----------
    def _boton(self, padre, texto, comando, color):
        boton = tk.Button(
            padre, text=texto, command=comando, font=tema.FUENTE_NEGRITA,
            bg=color, fg=tema.COLOR_TEXTO, activebackground=tema.COLOR_BOTON_HOVER,
            relief="flat", padx=12, pady=6, cursor="hand2",
        )
        self.botones.append(boton)
        return boton

    def _crear_formulario(self):
        marco = tk.Frame(self, bg=tema.COLOR_MARCO)
        marco.pack(fill="x", padx=15, pady=(15, 5))

        self.var_nombre = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_stock = tk.StringVar()
        self.var_activo = tk.BooleanVar(value=True)

        campos = [
            ("Nombre:", self.var_nombre, 0, 0, 28),
            ("Precio:", self.var_precio, 0, 2, 12),
            ("Stock:", self.var_stock, 0, 4, 8),
        ]
        for texto, variable, fila, col, ancho in campos:
            tk.Label(
                marco, text=texto, font=tema.FUENTE_NORMAL,
                bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO,
            ).grid(row=fila, column=col, padx=(10, 4), pady=6, sticky="e")
            entrada = tk.Entry(
                marco, textvariable=variable, width=ancho,
                font=tema.FUENTE_NORMAL, relief="solid", bd=1,
            )
            entrada.grid(row=fila, column=col + 1, padx=(0, 10), pady=6)
            entrada.bind("<Return>", lambda e: self.crear())
            if col == 0:
                self.entrada_nombre = entrada

        tk.Checkbutton(
            marco, text="Activo", variable=self.var_activo,
            font=tema.FUENTE_NORMAL, bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO,
            activebackground=tema.COLOR_MARCO, selectcolor=tema.COLOR_BLANCO,
        ).grid(row=0, column=6, padx=10)

        botones = tk.Frame(marco, bg=tema.COLOR_MARCO)
        botones.grid(row=1, column=0, columnspan=7, pady=(4, 8))

        self._boton(botones, "＋ Guardar nuevo", self.crear, tema.COLOR_VERDE).pack(side="left", padx=5)
        self._boton(botones, "✎ Actualizar", self.actualizar, tema.COLOR_BOTON).pack(side="left", padx=5)
        self._boton(botones, "⏻ Activar / Desactivar", self.alternar_activo, tema.COLOR_NARANJA).pack(side="left", padx=5)
        self._boton(botones, "🗑 Eliminar", self.eliminar, tema.COLOR_ALERTA).pack(side="left", padx=5)
        self._boton(botones, "✕ Limpiar", self.limpiar_formulario, tema.COLOR_FONDO).pack(side="left", padx=5)

    def _crear_barra_busqueda(self):
        barra = tk.Frame(self, bg=tema.COLOR_MARCO)
        barra.pack(fill="x", padx=15, pady=(5, 0))

        tk.Label(
            barra, text="Buscar:", font=tema.FUENTE_NORMAL,
            bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO,
        ).pack(side="left")

        self.texto_busqueda = tk.StringVar()
        self.texto_busqueda.trace_add("write", lambda *args: self._mostrar())
        tk.Entry(
            barra, textvariable=self.texto_busqueda, width=30,
            font=tema.FUENTE_NORMAL, relief="solid", bd=1,
        ).pack(side="left", padx=8)

        self._boton(barra, "↻  Recargar", self.cargar, tema.COLOR_BOTON).pack(side="right")

    def _crear_tabla(self):
        contenedor = tk.Frame(self, bg=tema.COLOR_MARCO)
        contenedor.pack(fill="both", expand=True, padx=15, pady=10)

        columnas = ("id", "nombre", "precio", "stock", "estado")
        self.tabla = ttk.Treeview(
            contenedor, columns=columnas, show="headings", selectmode="browse"
        )
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("stock", text="Stock")
        self.tabla.heading("estado", text="Estado")
        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("nombre", width=300, anchor="w")
        self.tabla.column("precio", width=120, anchor="e")
        self.tabla.column("stock", width=90, anchor="center")
        self.tabla.column("estado", width=110, anchor="center")

        self.tabla.tag_configure("bajo", background=tema.COLOR_NARANJA)
        self.tabla.tag_configure("agotado", background=tema.COLOR_ALERTA)
        self.tabla.tag_configure("inactivo", foreground=tema.COLOR_GRIS)

        scroll = ttk.Scrollbar(contenedor, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Evento: al elegir una fila, sus datos pasan al formulario
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)
        # Atajo: tecla Supr elimina el producto seleccionado
        self.tabla.bind("<Delete>", lambda e: self.eliminar())

    # ---------- Utilidades ----------
    def _bloquear(self, bloquear):
        estado = "disabled" if bloquear else "normal"
        for boton in self.botones:
            boton.config(state=estado)

    def _buscar(self, id_producto):
        for p in self.productos:
            if p["id"] == id_producto:
                return p
        return None

    def _al_seleccionar(self, evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        producto = self._buscar(int(seleccion[0]))
        if producto is None:
            return
        self.id_seleccionado = producto["id"]
        self.var_nombre.set(producto["nombre"])
        self.var_precio.set(str(float(producto["precio"])).rstrip("0").rstrip("."))
        self.var_stock.set(str(producto["stock"]))
        self.var_activo.set(producto["activo"])

    def limpiar_formulario(self):
        self.id_seleccionado = None
        self.var_nombre.set("")
        self.var_precio.set("")
        self.var_stock.set("")
        self.var_activo.set(True)
        self.tabla.selection_remove(self.tabla.selection())
        self.entrada_nombre.focus_set()

    def _leer_formulario(self):
        """Valida los campos y devuelve los datos listos para la API."""
        nombre = self.var_nombre.get().strip()
        precio_txt = self.var_precio.get().strip().replace(",", ".")
        stock_txt = self.var_stock.get().strip() or "0"

        if nombre == "":
            messagebox.showwarning("Falta el nombre", "Escribe el nombre del producto.")
            return None
        try:
            precio = float(precio_txt)
        except ValueError:
            messagebox.showwarning("Precio inválido", "El precio debe ser un número.")
            return None
        if precio <= 0:
            messagebox.showwarning("Precio inválido", "El precio debe ser mayor que cero.")
            return None
        if not stock_txt.isdigit():
            messagebox.showwarning("Stock inválido", "El stock debe ser un número entero (0 o más).")
            return None

        datos = {}
        datos["nombre"] = nombre
        datos["precio"] = "%.2f" % precio
        datos["stock"] = int(stock_txt)
        datos["activo"] = self.var_activo.get()
        return datos

    def _necesita_seleccion(self):
        if self.id_seleccionado is None:
            messagebox.showinfo("Elige un producto", "Primero selecciona un producto de la tabla.")
            return False
        return True

    # ---------- Datos (GET) ----------
    def cargar(self):
        self._bloquear(True)
        self.app.ejecutar(
            self.app.cliente.listar_productos,
            self._al_cargar,
            self._al_fallar,
            mensaje="Cargando productos...",
        )

    def _al_cargar(self, datos):
        self.productos = datos
        self._bloquear(False)
        self._mostrar()

    def _al_fallar(self, error):
        self._bloquear(False)
        if isinstance(error, ErrorAPI) and error.codigo == 409:
            messagebox.showwarning("No se puede eliminar", error.mensaje)
        else:
            self.app.mostrar_error(error)

    def _mostrar(self):
        self.tabla.delete(*self.tabla.get_children())
        filtro = self.texto_busqueda.get().strip().lower()

        for p in self.productos:
            if filtro and filtro not in p["nombre"].lower():
                continue

            if not p["activo"]:
                etiqueta, estado = "inactivo", "Inactivo"
            elif p["stock"] == 0:
                etiqueta, estado = "agotado", "Agotado"
            elif p["stock"] <= STOCK_BAJO:
                etiqueta, estado = "bajo", "Poco stock"
            else:
                etiqueta, estado = "", "Activo"

            valores = (p["id"], p["nombre"], formato_precio(p["precio"]),
                       p["stock"], estado)
            self.tabla.insert("", "end", iid=str(p["id"]), values=valores,
                              tags=(etiqueta,))

    # ---------- Acciones (POST, PUT, PATCH, DELETE) ----------
    def _accion(self, funcion, carga, exito):
        self._bloquear(True)

        def al_terminar(_resultado):
            self.limpiar_formulario()
            self.cargar()
            messagebox.showinfo("Listo", exito)

        self.app.ejecutar(funcion, al_terminar, self._al_fallar, mensaje=carga)

    def crear(self):                                   # POST
        datos = self._leer_formulario()
        if datos is None:
            return
        self._accion(
            lambda: self.app.cliente.crear_producto(datos),
            "Guardando producto...", "Producto guardado correctamente.",
        )

    def actualizar(self):                              # PUT
        if not self._necesita_seleccion():
            return
        datos = self._leer_formulario()
        if datos is None:
            return
        id_producto = self.id_seleccionado
        self._accion(
            lambda: self.app.cliente.editar_producto(id_producto, datos),
            "Actualizando producto...", "Producto actualizado correctamente.",
        )

    def alternar_activo(self):                         # PATCH
        if not self._necesita_seleccion():
            return
        id_producto = self.id_seleccionado
        producto = self._buscar(id_producto)
        nuevo = not producto["activo"]
        if nuevo:
            mensaje = "Producto activado."
        else:
            mensaje = "Producto desactivado (su historial se conserva)."
        self._accion(
            lambda: self.app.cliente.cambiar_activo(id_producto, nuevo),
            "Cambiando estado...", mensaje,
        )

    def eliminar(self):                                # DELETE
        if not self._necesita_seleccion():
            return
        id_producto = self.id_seleccionado
        producto = self._buscar(id_producto)
        pregunta = "¿Seguro que quieres eliminar «" + producto["nombre"] + "»?"
        if not messagebox.askyesno("Confirmar", pregunta):
            return
        self._accion(
            lambda: self.app.cliente.eliminar_producto(id_producto),
            "Eliminando producto...", "Producto eliminado.",
        )