import tkinter as tk
from datetime import datetime


class Camiseta:

    def __init__(self, ventana_Principal):
        self.id = None  
        self.ventana_Principal = ventana_Principal
        self.color = tk.StringVar(ventana_Principal)
        self.talla = tk.StringVar(ventana_Principal)
        self.fecha_creacion = tk.StringVar(ventana_Principal)
        self.material = tk.StringVar(ventana_Principal, value="ninguno")
        self.marca = tk.StringVar(ventana_Principal)

    def limpiar(self):
        self.id = None  # NUEVO: al limpiar, vuelve a "creando"
        self.color.set('')
        self.talla.set('')
        self.fecha_creacion.set('')
        self.material.set('ninguno')
        self.marca.set('')

    def cargar(self, datos):  # NUEVO: llena el formulario con una camiseta del backend
        self.id = datos['id']
        self.color.set(datos['color'])
        self.talla.set(datos['talla'])
        self.fecha_creacion.set(
            datetime.strptime(datos['fecha_creacion'], '%Y-%m-%d').strftime('%d/%m/%Y')
        )
        self.material.set(datos['material'])
        self.marca.set(datos['marca'])

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