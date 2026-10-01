import tkinter as tk
import tkinter.messagebox as messagebox
from zapato import Zapato

class Interfaz():
    def __init__(self):
        self.ventana_principal = tk.Tk()

    def accion_guardar_boton(self, marca):
        messagebox.showinfo("Guardar", f"Guardando: Marca: {marca}")

    def mostrar_interfaz(self):
        zapato = Zapato(self.ventana_principal)

        label_marca = tk.Label(self.ventana_principal, text="Marca del zapato: ")
        entry_marca = tk.Entry(self.ventana_principal, textvariable=zapato.marca)

        boton_guardar = tk.Button(self.ventana_principal, text="Guardar", command=lambda: self.accion_guardar_boton(entry_marca.get()))

        self.ventana_principal.title("Ventana principal")
        self.ventana_principal.geometry("300x300")
        
        label_marca.pack()
        entry_marca.pack()
        boton_guardar.pack()

        self.ventana_principal.mainloop()