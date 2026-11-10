import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import tema
from cliente_api import ClienteAPI, ErrorConexion, ErrorAPI
from pestana_productos import PestanaProductos
from pestana_ventas import PestanaVentas

COLOR_OK = "#2e8b57"
COLOR_ERROR = "#d64545"
CUADROS_CARGA = ["◐", "◓", "◑", "◒"]


class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Comercializadora El Cafetal")
        self.configure(bg=tema.COLOR_FONDO)
        self._ajustar_tamano()

        self.cliente = ClienteAPI()
        self._ocupados = 0
        self._animando = False
        self._cuadro = 0
        self._mensaje_carga = ""

        self._configurar_estilos()
        self._crear_barra_estado()
        self._crear_titulo()
        self._crear_pestanas()

        self.after(200, self.pestana_productos.cargar)

    # ---------- Ventana ----------
    def _ajustar_tamano(self):
        """Usa como máximo el 80% de la pantalla y centra la ventana."""
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        ancho = min(1100, int(ancho_pantalla * 0.85))
        alto = min(720, int(alto_pantalla * 0.85))
        x = (ancho_pantalla - ancho) // 2
        y = (alto_pantalla - alto) // 3
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.minsize(900, 520)

    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure("TNotebook", background=tema.COLOR_FONDO, borderwidth=0)
        estilo.configure("TNotebook.Tab", background=tema.COLOR_MARCO, foreground=tema.COLOR_TEXTO, font=tema.FUENTE_NEGRITA, padding=(24, 10), borderwidth=0)
        estilo.map("TNotebook.Tab", background=[("selected", tema.COLOR_BOTON)], foreground=[("selected", tema.COLOR_BLANCO)])
        estilo.configure("Marco.TFrame", background=tema.COLOR_MARCO)

        estilo.configure("Treeview", background=tema.COLOR_BLANCO, fieldbackground=tema.COLOR_BLANCO, foreground=tema.COLOR_TEXTO, font=tema.FUENTE_NORMAL, rowheight=30, borderwidth=0)
        estilo.map("Treeview", background=[("selected", tema.COLOR_BOTON)], foreground=[("selected", tema.COLOR_BLANCO)])
        estilo.configure("Treeview.Heading", background=tema.COLOR_BOTON, foreground=tema.COLOR_TEXTO, font=tema.FUENTE_NEGRITA, padding=6, relief="flat")
        estilo.map("Treeview.Heading", background=[("active", tema.COLOR_BOTON_HOVER)])

    def _crear_barra_estado(self):
        self.barra = tk.Label(
            self, text="●  Sin verificar", anchor="w", padx=15, pady=6,
            font=tema.FUENTE_PEQUENA, bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO,
        )
        self.barra.pack(fill="x", side="bottom")

    def _crear_titulo(self):
        tk.Label(
            self, text="Comercializadora El Cafetal", font=tema.FUENTE_TITULO,
            bg=tema.COLOR_FONDO, fg=tema.COLOR_TEXTO,
        ).pack(pady=(10, 0))

    def _crear_pestanas(self):
        self.pestanas = ttk.Notebook(self)
        self.pestanas.pack(fill="both", expand=True, padx=20, pady=10)

        self.pestana_productos = PestanaProductos(self.pestanas, self)
        self.pestana_ventas = PestanaVentas(self.pestanas, self)
        self.pestanas.add(self.pestana_productos, text="Productos")
        self.pestanas.add(self.pestana_ventas, text="Ventas")

        def al_cambiar(evento):
            actual = self.pestanas.select()
            if actual == str(self.pestana_ventas):
                self.pestana_ventas.refrescar()
            elif actual == str(self.pestana_productos):
                self.pestana_productos.cargar()

        self.pestanas.bind("<<NotebookTabChanged>>", al_cambiar)

    # ---------- Peticiones en segundo plano ----------
    def ejecutar(self, funcion, al_exito=None, al_error=None, mensaje="Cargando..."):
        """Corre 'funcion' en un hilo para no congelar la ventana."""
        resultado = queue.Queue()

        def trabajo():
            try:
                resultado.put(("ok", funcion()))
            except Exception as error:
                resultado.put(("error", error))

        self._ocupados += 1
        self._mensaje_carga = mensaje
        if not self._animando:
            self._animando = True
            self._animar()

        threading.Thread(target=trabajo, daemon=True).start()
        self._esperar(resultado, al_exito, al_error)

    def _esperar(self, resultado, al_exito, al_error):
        try:
            tipo, valor = resultado.get_nowait()
        except queue.Empty:
            self.after(50, lambda: self._esperar(resultado, al_exito, al_error))
            return

        self._ocupados -= 1
        if tipo == "ok":
            self._poner_estado("●  Conectado", COLOR_OK)
            if al_exito:
                al_exito(valor)
        else:
            if isinstance(valor, ErrorConexion):
                self._poner_estado("●  Servidor no disponible", COLOR_ERROR)
            else:
                self._poner_estado("●  Conectado", COLOR_OK)
            if al_error:
                al_error(valor)

    def _animar(self):
        if self._ocupados <= 0:
            self._animando = False
            return
        simbolo = CUADROS_CARGA[self._cuadro % len(CUADROS_CARGA)]
        self._poner_estado(f"{simbolo}  {self._mensaje_carga}", tema.COLOR_TEXTO)
        self._cuadro += 1
        self.after(120, self._animar)

    def _poner_estado(self, texto, color):
        self.barra.config(text=texto, fg=color)

    # ---------- Mensajes ----------
    def mostrar_error(self, error):
        if isinstance(error, ErrorConexion):
            messagebox.showerror(
                "Servidor no disponible",
                "No se pudo conectar con el servidor.\n"
                "Revisa que el backend esté encendido.",
            )
        elif isinstance(error, ErrorAPI):
            messagebox.showerror("No se pudo completar", error.mensaje)
        else:
            messagebox.showerror("Error inesperado", str(error))


if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()