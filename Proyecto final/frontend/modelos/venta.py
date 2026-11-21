import tkinter as tk


class Venta():

    METODOS = {
        'Efectivo': 'EFECTIVO',
        'Tarjeta': 'TARJETA',
        'Transferencia': 'TRANSFERENCIA',
    }

    def __init__(self, ventana_principal):
        self.id = None
        self.cliente = tk.StringVar(ventana_principal)
        self.metodo_pago = tk.StringVar(ventana_principal, value='Efectivo')
        self.observaciones = tk.StringVar(ventana_principal)

    def limpiar(self):
        self.id = None
        self.cliente.set('')
        self.metodo_pago.set('Efectivo')
        self.observaciones.set('')

    def cargar(self, datos):
        self.id = datos['id']
        self.cliente.set(datos['cliente'])
        for nombre, codigo in Venta.METODOS.items():
            if codigo == datos['metodo_pago']:
                self.metodo_pago.set(nombre)
        self.observaciones.set(datos['observaciones'])

    def a_diccionario(self):
        return {
            'cliente': self.cliente.get().strip(),
            'metodo_pago': Venta.METODOS[self.metodo_pago.get()],
            'observaciones': self.observaciones.get().strip(),
        }