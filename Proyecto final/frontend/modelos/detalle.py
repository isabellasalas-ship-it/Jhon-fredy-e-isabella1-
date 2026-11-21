import tkinter as tk


class Detalle():

    def __init__(self, ventana_principal):
        self.producto = tk.StringVar(ventana_principal)
        self.cantidad = tk.StringVar(ventana_principal, value='1')

    def limpiar(self):
        self.producto.set('')
        self.cantidad.set('1')

    def a_diccionario(self, id_venta, id_producto):
        return {
            'venta': id_venta,
            'producto': id_producto,
            'cantidad': int(self.cantidad.get().strip()),
        }