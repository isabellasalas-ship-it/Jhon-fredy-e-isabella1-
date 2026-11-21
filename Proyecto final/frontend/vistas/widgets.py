"""Piezas visuales propias: botones y cajas redondeadas y la cabecera con café."""
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

from vistas import tema


def oscurecer(color, factor):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    return "#%02x%02x%02x" % (int(r * factor), int(g * factor), int(b * factor))


def puntos_redondeados(x1, y1, x2, y2, r):
    r = max(0, min(r, (x2 - x1) / 2, (y2 - y1) / 2))
    return [
        x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1,
        x2, y1 + r, x2, y1 + r, x2, y2 - r, x2, y2 - r, x2, y2,
        x2 - r, y2, x2 - r, y2, x1 + r, y2, x1 + r, y2, x1, y2,
        x1, y2 - r, x1, y2 - r, x1, y1 + r, x1, y1 + r, x1, y1,
    ]


def poligono_redondo(canvas, x1, y1, x2, y2, r, **opciones):
    return canvas.create_polygon(
        puntos_redondeados(x1, y1, x2, y2, r), smooth=True, **opciones
    )


class BotonRedondo(tk.Canvas):
    """Botón con esquinas redondeadas, efecto al pasar el mouse y al presionar."""

    def __init__(self, padre, texto, comando, color=None, fondo=None,
                 padx=16, pady=7, radio=14):
        fuente = tkfont.Font(root=padre, font=tema.FUENTE_NEGRITA)
        ancho = fuente.measure(texto) + 2 * padx
        alto = fuente.metrics("linespace") + 2 * pady
        super().__init__(
            padre, width=ancho, height=alto, bg=fondo or tema.COLOR_MARCO,
            highlightthickness=0, bd=0, cursor="hand2",
        )
        self.b_color = color or tema.COLOR_BOTON
        self.b_comando = comando
        self.b_activo = True
        self.b_cx = ancho / 2
        self.b_cy = alto / 2

        self.b_forma = poligono_redondo(
            self, 1, 1, ancho - 1, alto - 1, radio, fill=self.b_color, outline=""
        )
        self.b_texto = self.create_text(
            self.b_cx, self.b_cy, text=texto, font=tema.FUENTE_NEGRITA,
            fill=tema.COLOR_TEXTO,
        )

        self.bind("<Enter>", self._entrar)
        self.bind("<Leave>", self._salir)
        self.bind("<ButtonPress-1>", self._presionar)
        self.bind("<ButtonRelease-1>", self._soltar)

    def _entrar(self, evento):
        if self.b_activo:
            self.itemconfigure(self.b_forma, fill=oscurecer(self.b_color, 0.94))

    def _salir(self, evento):
        if self.b_activo:
            self.itemconfigure(self.b_forma, fill=self.b_color)
            self.coords(self.b_texto, self.b_cx, self.b_cy)

    def _presionar(self, evento):
        if self.b_activo:
            self.itemconfigure(self.b_forma, fill=oscurecer(self.b_color, 0.86))
            self.coords(self.b_texto, self.b_cx, self.b_cy + 1)

    def _soltar(self, evento):
        if not self.b_activo:
            return
        self.itemconfigure(self.b_forma, fill=oscurecer(self.b_color, 0.94))
        self.coords(self.b_texto, self.b_cx, self.b_cy)
        dentro = (0 <= evento.x <= self.winfo_width()
                  and 0 <= evento.y <= self.winfo_height())
        if dentro and self.b_comando:
            self.b_comando()

    def activar(self, valor=True):
        self.b_activo = valor
        if valor:
            self.itemconfigure(self.b_forma, fill=self.b_color)
            self.itemconfigure(self.b_texto, fill=tema.COLOR_TEXTO)
            self.config(cursor="hand2")
        else:
            self.itemconfigure(self.b_forma, fill="#ddd5e6")
            self.itemconfigure(self.b_texto, fill="#a9a3b8")
            self.config(cursor="arrow")


class CajaRedonda(tk.Canvas):
    """Caja con esquinas redondeadas que contiene un campo (Entry o Combobox)."""

    def __init__(self, padre, crear_hijo, ancho=160, fondo=None, radio=13):
        fuente = tkfont.Font(root=padre, font=tema.FUENTE_NORMAL)
        alto = fuente.metrics("linespace") + 20
        super().__init__(
            padre, width=ancho, height=alto, bg=fondo or tema.COLOR_MARCO,
            highlightthickness=0, bd=0,
        )
        self.c_alto = alto
        self.c_radio = radio
        self.forma = poligono_redondo(
            self, 1, 1, ancho - 1, alto - 1, radio,
            fill=tema.COLOR_BLANCO, outline=tema.COLOR_BOTON, width=2,
        )
        self.hijo = crear_hijo(self)
        self.ventana = self.create_window(
            radio, alto / 2, window=self.hijo, anchor="w",
            width=max(10, ancho - 2 * radio),
        )
        self.bind("<Configure>", self._ajustar)
        self.hijo.bind(
            "<FocusIn>",
            lambda e: self.itemconfigure(self.forma, outline=tema.COLOR_FOCO),
        )
        self.hijo.bind(
            "<FocusOut>",
            lambda e: self.itemconfigure(self.forma, outline=tema.COLOR_BOTON),
        )

    def _ajustar(self, evento):
        self.coords(
            self.forma,
            *puntos_redondeados(1, 1, evento.width - 1, evento.height - 1, self.c_radio)
        )
        self.itemconfigure(self.ventana, width=max(10, evento.width - 2 * self.c_radio))


def entrada_redonda(padre, variable, ancho=160, fondo=None):
    def crear(canvas):
        return tk.Entry(
            canvas, textvariable=variable, font=tema.FUENTE_NORMAL, relief="flat",
            bd=0, bg=tema.COLOR_BLANCO, fg=tema.COLOR_TEXTO,
            insertbackground=tema.COLOR_TEXTO, highlightthickness=0,
        )
    return CajaRedonda(padre, crear, ancho=ancho, fondo=fondo)


def combo_redondo(padre, variable, valores=None, ancho=160, fondo=None):
    def crear(canvas):
        return ttk.Combobox(
            canvas, textvariable=variable, values=valores or [],
            state="readonly", font=tema.FUENTE_NORMAL, style="Redondo.TCombobox",
        )
    return CajaRedonda(padre, crear, ancho=ancho, fondo=fondo)


def dibujar_taza(canvas, cx, cy, s=1.0):
    """Dibuja una taza de café con vapor, centrada en (cx, cy)."""
    def p(dx, dy):
        return cx + dx * s, cy + dy * s

    grosor = max(2, int(3 * s))

    
    x1, y1 = p(-38, 24)
    x2, y2 = p(38, 34)
    canvas.create_oval(x1, y1, x2, y2, fill="#ffe3c4", outline="")

    
    x1, y1 = p(14, -8)
    x2, y2 = p(42, 18)
    canvas.create_arc(
        x1, y1, x2, y2, start=-90, extent=180, style="arc",
        outline=tema.COLOR_CREMA, width=max(3, int(6 * s)),
    )

    
    puntos = []
    for dx, dy in [(-27, -14), (27, -14), (25, 10), (16, 27), (-16, 27), (-25, 10)]:
        puntos.extend(p(dx, dy))
    canvas.create_polygon(puntos, smooth=True, fill=tema.COLOR_CREMA, outline="")

    
    x1, y1 = p(-27, -21)
    x2, y2 = p(27, -8)
    canvas.create_oval(
        x1, y1, x2, y2, fill=tema.COLOR_CAFE, outline=tema.COLOR_CREMA, width=grosor,
    )

    
    for dx in (-12, 0, 12):
        linea = []
        for ddx, ddy in [(0, -27), (-6, -35), (5, -43), (-4, -52)]:
            linea.extend(p(dx + ddx, ddy))
        canvas.create_line(
            linea, smooth=True, fill="#ffffff", width=grosor, capstyle="round",
        )


class Cabecera(tk.Canvas):
    """Franja de arriba con el título grande y tazas de café."""

    def __init__(self, padre, alto=112):
        super().__init__(
            padre, height=alto, bg=tema.COLOR_FONDO, highlightthickness=0, bd=0,
        )
        self.bind("<Configure>", self._dibujar)

    def _dibujar(self, evento):
        self.delete("all")
        ancho, alto = evento.width, evento.height
        margen = 14

        poligono_redondo(
            self, margen, 8, ancho - margen, alto - 8, 30,
            fill=tema.COLOR_BOTON, outline="",
        )
        poligono_redondo(
            self, margen + 7, 15, ancho - margen - 7, alto - 15, 24,
            fill="", outline="#d9c9fb", width=2,
        )

        if ancho >= 780:
            dibujar_taza(self, margen + 80, alto / 2 + 12, 0.95)
            dibujar_taza(self, ancho - margen - 80, alto / 2 + 12, 0.95)

        tamano = max(15, min(28, int(ancho / 38)))
        fuente = ("Comic Sans MS", tamano, "bold")
        cx = ancho / 2
        self.create_text(
            cx + 2, alto / 2 - 8 + 3, text="COMERCIALIZADORA EL CAFETAL",
            font=fuente, fill=tema.COLOR_TEXTO,
        )
        self.create_text(
            cx, alto / 2 - 8, text="COMERCIALIZADORA EL CAFETAL",
            font=fuente, fill=tema.COLOR_BLANCO,
        )
        self.create_text(
            cx, alto / 2 + 27, text="Caicedonia, Valle del Cauca",
            font=("Segoe UI", 10), fill="#f6efff",
        )