import tkinter as tk
import tkinter.messagebox as messagebox
from zapato import Zapato
from tkcalendar import DateEntry

class Interfaz():
    def __init__(self):
        self.ventana_principal = tk.Tk()

    def accion_guardar_boton(self, marca, modelo, talla, fecha_de_creacion):
        if not talla.isdecimal() or not (20 <= int(talla) <= 50):
            messagebox.showerror("Error", "La talla debe ser un número entre 20 y 50")
            return
        messagebox.showinfo("Guardar", f"Guardando: Marca: {marca}, Modelo: {modelo}, Talla: {int(talla)}, Fecha de creacion: {fecha_de_creacion}")

    def mostrar_interfaz(self):
        zapato = Zapato(self.ventana_principal)

        label_marca = tk.Label(self.ventana_principal, text="Marca del zapato: ")
        entry_marca = tk.Entry(self.ventana_principal, textvariable=zapato.marca)

        label_error_marca = tk.Label(self.ventana_principal, text="", fg="red")

        def validar_letras_marca(texto):
            for c in texto:
                if not (c.isalpha() or c == " "):
                    label_error_marca.config(text="Solo se permiten letras")
                    return False
            label_error_marca.config(text="")
            return True

        validacion_marca = self.ventana_principal.register(validar_letras_marca)
        entry_marca.config(validate="key", validatecommand=(validacion_marca, "%P"))

        label_modelo = tk.Label(self.ventana_principal, text="Modelo del zapato: ")
        entry_modelo = tk.Entry(self.ventana_principal, textvariable=zapato.modelo)

        label_error_modelo = tk.Label(self.ventana_principal, text="", fg="red")

        def validar_letras_modelo(texto):
            for c in texto:
                if not (c.isalpha() or c == " "):
                    label_error_modelo.config(text="Solo se permiten letras")
                    return False
            label_error_modelo.config(text="")
            return True

        validacion_modelo = self.ventana_principal.register(validar_letras_modelo)
        entry_modelo.config(validate="key", validatecommand=(validacion_modelo, "%P"))

        label_talla = tk.Label(self.ventana_principal, text="Talla del zapato: ")
        entry_talla = tk.Entry(self.ventana_principal, textvariable=zapato.talla)

        label_error_talla = tk.Label(self.ventana_principal, text="", fg="red")

        def validar_numeros_talla(texto):
            # Vacío permitido (para poder borrar), solo dígitos y máximo 2
            if texto == "" or (texto.isdecimal() and len(texto) <= 2):
                label_error_talla.config(text="")
                return True
            label_error_talla.config(text="Solo se permiten números (máximo 2 dígitos)")
            return False

        validacion_talla = self.ventana_principal.register(validar_numeros_talla)
        entry_talla.config(validate="key", validatecommand=(validacion_talla, "%P"))

        label_fecha = tk.Label(self.ventana_principal, text="Fecha de creación: ")
        fecha = DateEntry(
            self.ventana_principal,
            textvariable=zapato.fecha_de_creacion
        )

        boton_guardar = tk.Button(self.ventana_principal, text="Guardar", command=lambda: self.accion_guardar_boton(entry_marca.get(), entry_modelo.get(), entry_talla.get(), fecha.get()))

        self.ventana_principal.title("Ventana principal")
        self.ventana_principal.geometry("300x400")
        
        label_marca.pack()
        entry_marca.pack()
        label_error_marca.pack()

        label_modelo.pack()
        entry_modelo.pack()
        label_error_modelo.pack()

        label_talla.pack()
        entry_talla.pack()
        label_error_talla.pack()

        label_fecha.pack()
        fecha.pack()

        boton_guardar.pack()

        self.ventana_principal.mainloop()