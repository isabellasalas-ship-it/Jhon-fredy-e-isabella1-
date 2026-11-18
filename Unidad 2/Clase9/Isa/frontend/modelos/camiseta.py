import tkinter as tk
from datetime import datetime


class Camiseta:

    def __init__(self, ventana_Principal):
        self.ventana_Principal = ventana_Principal
        self.color = tk.StringVar(ventana_Principal)
        self.talla = tk.StringVar(ventana_Principal)
        self.fecha_creacion = tk.StringVar(ventana_Principal)
        self.material = tk.StringVar(ventana_Principal, value="ninguno")
        self.marca = tk.StringVar(ventana_Principal)

    def limpiar(self):
        self.color.set('')
        self.talla.set('')
        self.fecha_creacion.set('')
        self.material.set('ninguno')
        self.marca.set('')

    def a_diccionario(self):
        fecha = datetime.strptime(
            self.fecha_creacion.get().strip(), "%d/%m/%Y"
        ).strftime("%Y-%m-%d")

        return {
        'color': self.color.get().strip(),
        'talla': self.talla.get(),
        'fecha_creacion': fecha,
        'material': self.material.get(),
        'marca': self.marca.get().strip(),
    }