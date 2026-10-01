import tkinter as tk

class Zapato():
    def __init__(self, ventana_principal):
        
        self.ventana_principal = ventana_principal
        self.marca = tk.StringVar(ventana_principal)
        