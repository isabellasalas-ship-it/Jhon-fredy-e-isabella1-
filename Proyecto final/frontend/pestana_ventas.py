import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

import tema

METODOS = {
    "Efectivo": "EFECTIVO",
    "Tarjeta": "TARJETA",
    "Transferencia": "TRANSFERENCIA",
}


def dinero(valor):
    numero = float(valor)
    if numero.is_integer():
        return f"${numero:,.0f}"
    return f"${numero:,.2f}"


def formato_fecha(texto):
    try:
        fecha = datetime.fromisoformat(texto).astimezone()
        return fecha.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return texto


class PestanaVentas(ttk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, style="Marco.TFrame")
        self.app = app
        self.productos = []
        self.ventas = []
        self.detalles = []
        self.opciones = []
        self.id_venta = None
        self.botones = []

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._crear_panel_ventas()
        self._crear_panel_detalles()

    # ---------- Piezas reutilizables ----------
    def _titulo(self, padre, texto):
        tk.Label(
            padre, text=texto, font=tema.FUENTE_NEGRITA,
            bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO,
        ).pack(anchor="w", pady=(0, 6))

    def _etiqueta(self, padre, texto):
        return tk.Label(
            padre, text=texto, font=tema.FUENTE_NORMAL,
            bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO,
        )

    def _entrada(self, padre, variable, ancho=None):
        entrada = tk.Entry(
            padre, textvariable=variable, font=tema.FUENTE_NORMAL,
            relief="solid", bd=1,
        )
        if ancho:
            entrada.config(width=ancho)
        return entrada

    def _boton(self, padre, texto, comando, color):
        boton = tk.Button(
            padre, text=texto, command=comando, font=tema.FUENTE_NEGRITA,
            bg=color, fg=tema.COLOR_TEXTO, activebackground=tema.COLOR_BOTON_HOVER,
            relief="flat", padx=10, pady=5, cursor="hand2",
        )
        self.botones.append(boton)
        return boton

    # ---------- Panel izquierdo: ventas ----------
    def _crear_panel_ventas(self):
        panel = tk.Frame(self, bg=tema.COLOR_MARCO)
        panel.grid(row=0, column=0, sticky="nsew", padx=(15, 7), pady=12)

        self._titulo(panel, "1. Venta")

        form = tk.Frame(panel, bg=tema.COLOR_MARCO)
        form.pack(fill="x")
        form.columnconfigure(1, weight=1)

        self.var_cliente = tk.StringVar()
        self.var_pago = tk.StringVar(value="Efectivo")
        self.var_obs = tk.StringVar()

        self._etiqueta(form, "Cliente:").grid(row=0, column=0, sticky="e", pady=3)
        self.entrada_cliente = self._entrada(form, self.var_cliente)
        self.entrada_cliente.grid(row=0, column=1, sticky="ew", padx=6, pady=3)
        self.entrada_cliente.bind("<Return>", lambda e: self.crear_venta())

        self._etiqueta(form, "Pago:").grid(row=1, column=0, sticky="e", pady=3)
        self.combo_pago = ttk.Combobox(
            form, textvariable=self.var_pago, values=list(METODOS.keys()),
            state="readonly", font=tema.FUENTE_NORMAL,
        )
        self.combo_pago.grid(row=1, column=1, sticky="ew", padx=6, pady=3)

        self._etiqueta(form, "Notas:").grid(row=2, column=0, sticky="e", pady=3)
        self._entrada(form, self.var_obs).grid(row=2, column=1, sticky="ew", padx=6, pady=3)

        botones = tk.Frame(panel, bg=tema.COLOR_MARCO)
        botones.pack(fill="x", pady=8)
        self._boton(botones, "＋ Crear venta", self.crear_venta, tema.COLOR_VERDE).pack(side="left")
        self._boton(botones, "Eliminar venta", self.eliminar_venta, tema.COLOR_ALERTA).pack(side="left", padx=8)

        contenedor = tk.Frame(panel, bg=tema.COLOR_MARCO)
        contenedor.pack(fill="both", expand=True)

        self.tabla_ventas = ttk.Treeview(
            contenedor, columns=("id", "fecha", "cliente", "total"),
            show="headings", selectmode="browse", height=6,
        )
        self.tabla_ventas.heading("id", text="N°")
        self.tabla_ventas.heading("fecha", text="Fecha")
        self.tabla_ventas.heading("cliente", text="Cliente")
        self.tabla_ventas.heading("total", text="Total")
        self.tabla_ventas.column("id", width=40, anchor="center")
        self.tabla_ventas.column("fecha", width=110, anchor="center")
        self.tabla_ventas.column("cliente", width=120, anchor="w")
        self.tabla_ventas.column("total", width=80, anchor="e")

        scroll = ttk.Scrollbar(contenedor, orient="vertical", command=self.tabla_ventas.yview)
        self.tabla_ventas.configure(yscrollcommand=scroll.set)
        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Evento: al elegir una venta se cargan sus productos
        self.tabla_ventas.bind("<<TreeviewSelect>>", self._al_seleccionar_venta)

    # ---------- Panel derecho: detalles ----------
    def _crear_panel_detalles(self):
        panel = tk.Frame(self, bg=tema.COLOR_MARCO)
        panel.grid(row=0, column=1, sticky="nsew", padx=(7, 15), pady=12)

        self._titulo(panel, "2. Productos de la venta")

        self.lbl_venta = tk.Label(
            panel, text="Elige o crea una venta", font=tema.FUENTE_PEQUENA,
            bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO, anchor="w",
        )
        self.lbl_venta.pack(fill="x")

        self.var_producto = tk.StringVar()
        self.combo_producto = ttk.Combobox(
            panel, textvariable=self.var_producto, state="readonly",
            font=tema.FUENTE_NORMAL,
        )
        self.combo_producto.pack(fill="x", pady=(4, 0))

        fila = tk.Frame(panel, bg=tema.COLOR_MARCO)
        fila.pack(fill="x", pady=6)
        self._etiqueta(fila, "Cantidad:").pack(side="left")
        self.var_cantidad = tk.StringVar(value="1")
        entrada = self._entrada(fila, self.var_cantidad, 6)
        entrada.pack(side="left", padx=6)
        entrada.bind("<Return>", lambda e: self.agregar_detalle())
        self._boton(fila, "＋ Agregar", self.agregar_detalle, tema.COLOR_VERDE).pack(side="left", padx=4)
        self._boton(fila, "Quitar", self.quitar_detalle, tema.COLOR_NARANJA).pack(side="left", padx=4)

        contenedor = tk.Frame(panel, bg=tema.COLOR_MARCO)
        contenedor.pack(fill="both", expand=True)

        self.tabla_det = ttk.Treeview(
            contenedor, columns=("producto", "cantidad", "precio", "subtotal"),
            show="headings", selectmode="browse", height=6,
        )
        self.tabla_det.heading("producto", text="Producto")
        self.tabla_det.heading("cantidad", text="Cant.")
        self.tabla_det.heading("precio", text="Precio")
        self.tabla_det.heading("subtotal", text="Subtotal")
        self.tabla_det.column("producto", width=130, anchor="w")
        self.tabla_det.column("cantidad", width=50, anchor="center")
        self.tabla_det.column("precio", width=80, anchor="e")
        self.tabla_det.column("subtotal", width=90, anchor="e")

        scroll = ttk.Scrollbar(contenedor, orient="vertical", command=self.tabla_det.yview)
        self.tabla_det.configure(yscrollcommand=scroll.set)
        self.tabla_det.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.lbl_total = tk.Label(
            panel, text="Total: $0", font=("Segoe UI", 18, "bold"),
            bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO, anchor="e",
        )
        self.lbl_total.pack(fill="x", pady=(8, 0))

    # ---------- Utilidades ----------
    def _bloquear(self, bloquear):
        estado = "disabled" if bloquear else "normal"
        for boton in self.botones:
            boton.config(state=estado)

    def _nombre_producto(self, id_producto):
        for p in self.productos:
            if p["id"] == id_producto:
                return p["nombre"]
        return f"Producto {id_producto}"

    def _al_fallar(self, error):
        self._bloquear(False)
        self.app.mostrar_error(error)

    # ---------- Cargar datos (GET) ----------
    def refrescar(self):
        id_venta = self.id_venta
        cliente = self.app.cliente

        def traer():
            datos = {
                "productos": cliente.listar_productos(),
                "ventas": cliente.listar_ventas(),
                "detalles": [],
            }
            if id_venta is not None:
                datos["detalles"] = cliente.listar_detalles(id_venta)
            return datos

        self._bloquear(True)
        self.app.ejecutar(traer, self._al_refrescar, self._al_fallar,
                          mensaje="Cargando ventas...")

    def _al_refrescar(self, datos):
        self.productos = datos["productos"]
        self.ventas = datos["ventas"]
        self.detalles = datos["detalles"]
        self._bloquear(False)
        self._mostrar_ventas()
        self._mostrar_detalles()
        self._llenar_combo()

    def cargar_detalles(self):
        id_venta = self.id_venta
        self.app.ejecutar(
            lambda: self.app.cliente.listar_detalles(id_venta),
            self._al_cargar_detalles, self._al_fallar,
            mensaje="Cargando productos de la venta...",
        )

    def _al_cargar_detalles(self, datos):
        self.detalles = datos
        self._mostrar_detalles()

    # ---------- Mostrar en pantalla ----------
    def _mostrar_ventas(self):
        self.tabla_ventas.delete(*self.tabla_ventas.get_children())
        for v in self.ventas:
            valores = (v["id"], formato_fecha(v["fecha"]), v["cliente"], dinero(v["total"]))
            self.tabla_ventas.insert("", "end", iid=str(v["id"]), values=valores)

        if self.id_venta is not None and self.tabla_ventas.exists(str(self.id_venta)):
            self.tabla_ventas.selection_set(str(self.id_venta))
            self.tabla_ventas.see(str(self.id_venta))

    def _mostrar_detalles(self):
        self.tabla_det.delete(*self.tabla_det.get_children())
        total = 0
        for d in self.detalles:
            subtotal = d["cantidad"] * float(d["precio_unitario"])
            total += subtotal
            valores = (self._nombre_producto(d["producto"]), d["cantidad"],
                       dinero(d["precio_unitario"]), dinero(subtotal))
            self.tabla_det.insert("", "end", iid=str(d["id"]), values=valores)

        self.lbl_total.config(text="Total: " + dinero(total))

        if self.id_venta is None:
            self.lbl_venta.config(text="Elige o crea una venta")
        else:
            nombre = ""
            for v in self.ventas:
                if v["id"] == self.id_venta:
                    nombre = v["cliente"]
            self.lbl_venta.config(text=f"Venta N° {self.id_venta}  ·  {nombre}")

    def _llenar_combo(self):
        # Solo productos activos y con existencias
        self.opciones = [p for p in self.productos if p["activo"] and p["stock"] > 0]
        textos = []
        for p in self.opciones:
            textos.append(f'{p["nombre"]}  —  {dinero(p["precio"])}  (quedan {p["stock"]})')
        self.combo_producto["values"] = textos
        self.var_producto.set("")

    # ---------- Evento de selección ----------
    def _al_seleccionar_venta(self, evento):
        seleccion = self.tabla_ventas.selection()
        if not seleccion:
            return
        id_venta = int(seleccion[0])
        if id_venta == self.id_venta:
            return
        self.id_venta = id_venta
        self.cargar_detalles()

    # ---------- Acciones (POST y DELETE) ----------
    def crear_venta(self):
        cliente = self.var_cliente.get().strip()
        if cliente == "":
            messagebox.showwarning("Falta el cliente", "Escribe el nombre del cliente.")
            return

        datos = {
            "cliente": cliente,
            "metodo_pago": METODOS[self.var_pago.get()],
            "observaciones": self.var_obs.get().strip(),
        }

        def al_terminar(venta):
            self.id_venta = venta["id"]
            self.var_cliente.set("")
            self.var_obs.set("")
            self.refrescar()

        self._bloquear(True)
        self.app.ejecutar(
            lambda: self.app.cliente.crear_venta(datos),
            al_terminar, self._al_fallar, mensaje="Creando venta...",
        )

    def eliminar_venta(self):
        if self.id_venta is None:
            messagebox.showinfo("Elige una venta", "Primero selecciona una venta de la tabla.")
            return
        id_venta = self.id_venta
        if not messagebox.askyesno(
            "Confirmar", f"¿Seguro que quieres eliminar la venta N° {id_venta}?"
        ):
            return

        def al_terminar(_resultado):
            self.id_venta = None
            self.refrescar()
            messagebox.showinfo("Listo", "Venta eliminada.")

        self._bloquear(True)
        self.app.ejecutar(
            lambda: self.app.cliente.eliminar_venta(id_venta),
            al_terminar, self._al_fallar, mensaje="Eliminando venta...",
        )

    def agregar_detalle(self):
        if self.id_venta is None:
            messagebox.showinfo("Elige una venta", "Primero crea o selecciona una venta.")
            return
        indice = self.combo_producto.current()
        if indice < 0:
            messagebox.showwarning("Falta el producto", "Elige un producto de la lista.")
            return

        producto = self.opciones[indice]
        texto = self.var_cantidad.get().strip()
        if not texto.isdigit() or int(texto) <= 0:
            messagebox.showwarning("Cantidad inválida", "La cantidad debe ser un número mayor que cero.")
            return
        cantidad = int(texto)
        if cantidad > producto["stock"]:
            messagebox.showwarning(
                "Sin existencias",
                f"Solo hay {producto['stock']} unidades de {producto['nombre']}.",
            )
            return

        datos = {"venta": self.id_venta, "producto": producto["id"], "cantidad": cantidad}

        def al_terminar(_resultado):
            self.var_cantidad.set("1")
            self.refrescar()

        self._bloquear(True)
        self.app.ejecutar(
            lambda: self.app.cliente.crear_detalle(datos),
            al_terminar, self._al_fallar, mensaje="Agregando producto...",
        )

    def quitar_detalle(self):
        seleccion = self.tabla_det.selection()
        if not seleccion:
            messagebox.showinfo("Elige un producto", "Selecciona en la tabla el producto que quieres quitar.")
            return
        id_detalle = int(seleccion[0])

        def al_terminar(_resultado):
            self.refrescar()

        self._bloquear(True)
        self.app.ejecutar(
            lambda: self.app.cliente.eliminar_detalle(id_detalle),
            al_terminar, self._al_fallar, mensaje="Quitando producto...",
        )