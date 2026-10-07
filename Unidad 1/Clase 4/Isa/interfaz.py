import tkinter as tk
import tkinter.messagebox as messagebox
from camiseta import Camiseta
from tkinter import ttk
from tkcalendar import DateEntry
import re


def validar_color(valor):
    patron = re.compile("^[a-zA-Z]+$")
    resultado = patron.match(valor.get()) is not None
    if not resultado:
        return False
    return True

class Interfaz():
    def __init__(self):
        self.ventana_principal = tk.Tk()
    def accion_guardar_boton(self,color,talla,fecha_creacion,material):
        messagebox.showinfo("Guardar", f"Guardado : Color {color}, Talla {talla}, Fecha {fecha_creacion}, Material {material}")


    def mostrar_Interfaz(self):
            clase=Camiseta(self.ventana_principal)

            label_color = tk.Label(self.ventana_principal, text="Color de la camiseta")
            entry_color = tk.Entry(self.ventana_principal, textvariable=clase.color)
            label_talla = tk.Label(self.ventana_principal, text="Talla de la camiseta")

            combo_talla = ttk.Combobox(
            self.ventana_principal,
            textvariable=clase.talla,
            values=["S", "M", "L", "XL"]
            )


            label_fecha = tk.Label(
            self.ventana_principal,
            text="Fecha de creación"
            )
            fecha = DateEntry(
            self.ventana_principal,
            textvariable=clase.fecha_creacion
            )

            label_material = tk.Label(
            self.ventana_principal,
            text="Material de la camiseta"
)

            radio_algodon = tk.Radiobutton(
            self.ventana_principal,
            text="Algodón",
            variable=clase.material,
            value="Algodón"
)

            radio_poliester = tk.Radiobutton(
            self.ventana_principal,
            text="Poliéster",
            variable=clase.material,
            value="Poliéster"
            )

            radio_lana = tk.Radiobutton(
            self.ventana_principal,
            text="Lana",
            variable=clase.material,
            value="Lana"
            )



            boton_guardar= tk.Button(self.ventana_principal,
                          text="Guardar",
                          command=lambda: self.accion_guardar_boton(clase.color.get(), clase.talla.get(), clase.fecha_creacion.get(), clase.material.get()))
                            
            self.ventana_principal.title("Ventana Principal")
            self.ventana_principal.geometry("300x300")
            label_color.pack()
            entry_color.pack()
           

            label_talla.pack()
            combo_talla.pack()

            label_fecha.pack()
            fecha.pack()   

            label_material.pack()
            radio_algodon.pack()
            radio_poliester.pack()
            radio_lana.pack()

            boton_guardar.pack()
           

            self.ventana_principal.mainloop()