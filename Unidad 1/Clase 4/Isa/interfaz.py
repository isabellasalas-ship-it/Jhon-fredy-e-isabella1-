import tkinter as tk
import tkinter.messagebox as messagebox
from camiseta import Camiseta
from tkinter import ttk
from tkcalendar import DateEntry
import re



class Interfaz():
    def __init__(self):
        self.ventana_principal = tk.Tk()
        self.ventana_principal.configure(bg="lightblue")# PROFE ESTO FUE OPCIONAL, SOLO PARA DARLE COLOR A LA VENTANA PRINCIPAL
    
    def accion_guardar_boton(self, color, talla, fecha_creacion, material):
        if not color.strip():
             messagebox.showerror("Error", "Ingrese el color de la camiseta")
             return

        if talla.upper() not in ["S", "M", "L", "XL"]:
            messagebox.showerror("Error", "Seleccione una talla válida: S, M, L o XL")
            return

        if not material:
            messagebox.showerror("Error", "Seleccione el  material de la camiseta")
            return

        messagebox.showinfo(
        "Guardar",
        f"Guardado:\nColor: {color}\nTalla: {talla}\n"
        f"Fecha: {fecha_creacion}\nMaterial: {material}"
    )


    def mostrar_Interfaz(self):
            clase=Camiseta(self.ventana_principal)
            

            label_color = tk.Label(self.ventana_principal, text="Color de la camiseta",bg="lightblue")# ESTO TAMBIEN FUE OPCIONAL, SE VEIA TODO MUY JUNTO
            entry_color = tk.Entry(self.ventana_principal, textvariable=clase.color)

            label_error_color = tk.Label(self.ventana_principal, text="", fg="red",bg="lightblue")

            def validar_letras_color(texto):
                for c in texto:
                    if not (c.isalpha() or c == " "):
                        label_error_color.config(text="Solo se permiten letras")
                        return False
                label_error_color.config(text="")
                return True

            validacion_color = self.ventana_principal.register(validar_letras_color)
            entry_color.config(validate="key", validatecommand=(validacion_color, "%P"))

            label_talla = tk.Label(self.ventana_principal, text="Talla de la camiseta",bg="lightblue")

            combo_talla = ttk.Combobox(
            self.ventana_principal,
            textvariable=clase.talla,
            values=["S", "M", "L", "XL"]
            )

            label_error_talla = tk.Label(self.ventana_principal, text="", fg="red",bg="lightblue")

            def validar_talla(texto):
                tallas = ["S", "M", "L", "XL"]
                for t in tallas:
                    if t.startswith(texto.upper()):
                        label_error_talla.config(text="")
                        return True
                label_error_talla.config(text="Talla no válida. Use S, M, L o XL",bg="lightblue")
                return False

            validacion_talla = self.ventana_principal.register(validar_talla)
            combo_talla.config(validate="key", validatecommand=(validacion_talla, "%P"))


            label_fecha = tk.Label(
            self.ventana_principal,
            text="Fecha de creación",
            bg="lightblue"
            )
            fecha = DateEntry(
            self.ventana_principal,
            textvariable=clase.fecha_creacion
            )

            label_material = tk.Label(
            self.ventana_principal,
            text="Material de la camiseta",
            bg="lightblue"
            )

            radio_algodon = tk.Radiobutton(
            self.ventana_principal,
            text="Algodón",
            variable=clase.material,
            value="Algodón",
            bg="lightblue"
)

            radio_poliester = tk.Radiobutton(
            self.ventana_principal,
            text="Poliéster",
            variable=clase.material,
            value="Poliéster",
            bg="lightblue"
            )


            
            radio_lana = tk.Radiobutton(
            self.ventana_principal,
            text="Lana",
            variable=clase.material,
            value="Lana",
            bg="lightblue"
)


            boton_guardar= tk.Button(self.ventana_principal,
                          text="Guardar",
                          command=lambda: self.accion_guardar_boton(clase.color.get(), clase.talla.get(), clase.fecha_creacion.get(), clase.material.get()))
                            
            self.ventana_principal.title("Ventana Principal")
            self.ventana_principal.geometry("300x360")
            label_color.pack()
            entry_color.pack()
            label_error_color.pack()
           

            label_talla.pack()
            combo_talla.pack()
            label_error_talla.pack()

            label_fecha.pack()
            fecha.pack()   

            label_material.pack()
            radio_algodon.pack()
            radio_poliester.pack()
            radio_lana.pack()

            boton_guardar.pack()
           

            self.ventana_principal.mainloop()