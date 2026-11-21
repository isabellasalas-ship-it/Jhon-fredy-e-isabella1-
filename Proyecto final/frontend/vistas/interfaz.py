import queue
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

from controladores.comunicacion import Comunicacion, ErrorComunicacion
from vistas import tema
from vistas.estilos import aplicar_estilos
from vistas.vista_productos import VistaProductos
from vistas.vista_ventas import VistaVentas
from vistas.widgets import Cabecera

COLOR_OK = '#2e8b57'
COLOR_ERROR = '#d64545'
CUADROS_CARGA = ['◐', '◓', '◑', '◒']


class Interfaz():

    def __init__(self):
        self.ventana_principal = tk.Tk()
        self.comunicacion = Comunicacion()
        self.ocupados = 0
        self.animando = False
        self.cuadro = 0
        self.mensaje_carga = ''

  
    def ajustar_tamano(self):
        """Usa como máximo el 85% de la pantalla y centra la ventana."""
        ventana = self.ventana_principal
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        ancho = min(1100, int(ancho_pantalla * 0.85))
        alto = min(740, int(alto_pantalla * 0.88))
        x = (ancho_pantalla - ancho) // 2
        y = (alto_pantalla - alto) // 3
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
        ventana.minsize(900, 560)

    def crear_barra_estado(self):
        marco = tk.Frame(self.ventana_principal, bg=tema.COLOR_MARCO)
        marco.pack(fill='x', side='bottom')

        self.barra = tk.Label(
            marco, text='●  Sin verificar', anchor='w', padx=15, pady=6,
            font=tema.FUENTE_PEQUENA, bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO,
        )
        self.barra.pack(side='left')

        self.progreso = ttk.Progressbar(
            marco, mode='indeterminate', length=170,
            style='Cafe.Horizontal.TProgressbar',
        )

    def crear_pestanas(self):
        self.pestanas = ttk.Notebook(self.ventana_principal)
        self.pestanas.pack(fill='both', expand=True, padx=20, pady=10)

        self.vista_productos = VistaProductos(self.pestanas, self)
        self.vista_ventas = VistaVentas(self.pestanas, self)
        self.pestanas.add(self.vista_productos, text='Productos')
        self.pestanas.add(self.vista_ventas, text='Ventas')

        # Evento: al cambiar de pestaña, la nueva consulta lo que hay en el servidor
        self.pestanas.bind('<<NotebookTabChanged>>', self.al_cambiar_pestana)

    def al_cambiar_pestana(self, evento):
        pestana = self.pestanas.nametowidget(self.pestanas.select())
        pestana.refrescar()

    def al_cerrar(self):
        if messagebox.askyesno('Salir', '¿Seguro que quieres cerrar la aplicación?'):
            self.ventana_principal.destroy()

    def mostrar_interfaz(self):
        ventana = self.ventana_principal
        ventana.title('Comercializadora El Cafetal')
        ventana.configure(bg=tema.COLOR_FONDO)
        self.ajustar_tamano()
        aplicar_estilos(ventana)

        self.crear_barra_estado()
        Cabecera(ventana).pack(fill='x', padx=6, pady=(6, 0))
        self.crear_pestanas()

        ventana.protocol('WM_DELETE_WINDOW', self.al_cerrar)
        ventana.after(200, self.vista_productos.refrescar)
        ventana.mainloop()

    
    def ejecutar(self, funcion, al_exito=None, al_error=None,
                 mensaje='Cargando...', minimo=0.0):
        """Corre 'funcion' en un hilo para que la ventana no se congele.

        'minimo' son los segundos que se muestra la animación de carga,
        aunque el servidor responda más rápido (así se alcanza a ver).
        """
        resultado = queue.Queue()
        inicio = time.monotonic()

        def trabajo():
            try:
                resultado.put(('ok', funcion()))
            except Exception as error:
                resultado.put(('error', error))

        self.ocupados += 1
        self.mensaje_carga = mensaje
        if not self.animando:
            self.animando = True
            self.progreso.pack(side='right', padx=15, pady=5)
            self.progreso.start(12)
            self.animar()

        threading.Thread(target=trabajo, daemon=True).start()
        self.esperar(resultado, al_exito, al_error, inicio, minimo)

    def esperar(self, resultado, al_exito, al_error, inicio, minimo):
        try:
            tipo, valor = resultado.get_nowait()
        except queue.Empty:
            self.ventana_principal.after(
                50, lambda: self.esperar(resultado, al_exito, al_error, inicio, minimo)
            )
            return

        falta = minimo - (time.monotonic() - inicio)
        if falta > 0:
            self.ventana_principal.after(
                int(falta * 1000),
                lambda: self.terminar(tipo, valor, al_exito, al_error),
            )
        else:
            self.terminar(tipo, valor, al_exito, al_error)

    def terminar(self, tipo, valor, al_exito, al_error):
        self.ocupados -= 1
        if tipo == 'ok':
            self.poner_estado('●  Conectado', COLOR_OK)
            if al_exito:
                al_exito(valor)
            return

        sin_servidor = isinstance(valor, ErrorComunicacion) and valor.codigo is None
        if sin_servidor:
            self.poner_estado('●  Servidor no disponible', COLOR_ERROR)
        else:
            self.poner_estado('●  Conectado', COLOR_OK)
        if al_error:
            al_error(valor)

    def animar(self):
        if self.ocupados <= 0:
            self.animando = False
            self.progreso.stop()
            self.progreso.pack_forget()
            return
        simbolo = CUADROS_CARGA[self.cuadro % len(CUADROS_CARGA)]
        self.poner_estado(simbolo + '  ' + self.mensaje_carga, tema.COLOR_TEXTO)
        self.cuadro += 1
        self.ventana_principal.after(120, self.animar)

    def poner_estado(self, texto, color):
        self.barra.config(text=texto, fg=color)

    
    def mostrar_error(self, error):
        if isinstance(error, ErrorComunicacion):
            if error.codigo is None:
                messagebox.showerror('Servidor no disponible', str(error))
            elif error.codigo == 409:
                messagebox.showwarning('No se puede completar', str(error))
            else:
                messagebox.showerror('No se pudo completar', str(error))
        else:
            messagebox.showerror('Error inesperado', str(error))