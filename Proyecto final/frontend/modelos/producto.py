import tkinter as tk
from decimal import Decimal


class Producto():

    def __init__(self, ventana_principal):
        self.id = None
        self.nombre = tk.StringVar(ventana_principal)
        self.precio = tk.StringVar(ventana_principal)
        self.stock = tk.StringVar(ventana_principal)
        self.activo = tk.BooleanVar(ventana_principal, value=True)

    def limpiar(self):
        self.id = None
        self.nombre.set('')
        self.precio.set('')
        self.stock.set('')
        self.activo.set(True)

    def cargar(self, datos):
        self.id = datos['id']
        self.nombre.set(datos['nombre'])
        self.precio.set(format(Decimal(datos['precio']).normalize(), 'f'))
        self.stock.set(datos['stock'])
        self.activo.set(datos['activo'])

    def a_diccionario(self):
        precio = Decimal(self.precio.get().strip().replace(',', '.'))
        return {
            'nombre': self.nombre.get().strip(),
            'precio': str(precio.quantize(Decimal('0.01'))),
            'stock': int(self.stock.get().strip() or '0'),
            'activo': self.activo.get(),
        }