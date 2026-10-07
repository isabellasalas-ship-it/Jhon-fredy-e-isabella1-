import tkinter as tk

class Camiseta:

    def __init__(self, ventana_Principal):
        self.ventana_Principal = ventana_Principal
        self.color = tk.StringVar(ventana_Principal)
        self.talla= tk.StringVar(ventana_Principal)
        self.fecha_creacion= tk.StringVar(ventana_Principal)
        self.material= tk.StringVar(ventana_Principal)