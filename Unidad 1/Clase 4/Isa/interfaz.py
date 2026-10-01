import tkinter as tk
import tkinter.messagebox as messagebox
from camiseta import Camiseta

class Interfaz():
    def __init__(self):
        self.ventana_principal = tk.Tk()
    def accion_guardar_boton(self,color):
        messagebox.showinfo("Guardar", f"Guardado : Color {color}")


    def mostrar_Interfaz(self):
            clase=Camiseta(self.ventana_principal)

            label_color = tk.Label(self.ventana_principal, text="Color de la camiseta")
            entry_color = tk.Entry(self.ventana_principal, textvariable=clase.color)

            boton_guardar= tk.Button(self.ventana_principal,
                          text="Guardar",
                          command=lambda: self.accion_guardar_boton(clase.color.get()))

            self.ventana_principal.title("Ventana Principal")
            self.ventana_principal.geometry("300x300")
            label_color.pack()
            entry_color.pack()
            boton_guardar.pack()

            self.ventana_principal.mainloop()