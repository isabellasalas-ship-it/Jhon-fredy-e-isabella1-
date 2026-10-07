import tkinter as tk

class Zapato():
    def __init__(self, ventana_principal):
        
        self.ventana_principal = ventana_principal
        self.marca = tk.StringVar(ventana_principal)
        self.modelo = tk.StringVar(ventana_principal)
        self.talla = tk.StringVar(ventana_principal)
        self.fecha_de_creacion = tk.StringVar(ventana_principal)