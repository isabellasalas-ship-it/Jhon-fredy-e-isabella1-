import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from tkcalendar import DateEntry

from controladores.validaciones import Validaciones
from modelos.camiseta import Camiseta
from controladores.comunicacion import Comunicacion, ErrorComunicacion

ROJO = "red"
FONDO = "lightblue"


class Interfaz():

    def __init__(self):
        self.ventana_principal = tk.Tk()
        self.ventana_principal.configure(bg=FONDO)
        self.camiseta = Camiseta(self.ventana_principal)
        self.comunicacion = Comunicacion()
        self.labels_error = []

    def al_soltar_tecla(self, validacion, label_error):
        label_error.config(text=validacion() or "")

    def accion_guardar(self):
        errores = Validaciones.validarCamiseta(self.camiseta)

        if errores:
            messagebox.showwarning("Revise los datos", "\n".join(errores))
            return

        try:
            creada = self.comunicacion.crear(
                "camisetas", self.camiseta.a_diccionario()
            )
        except ErrorComunicacion as error:
            messagebox.showerror("No se pudo guardar", str(error))
            return

        messagebox.showinfo(
            "Guardado",
            "Camiseta " + creada["color"] +
            " guardada con el id " + str(creada["id"]) + "."
        )
        self.accion_limpiar()

    def accion_limpiar(self):
        self.camiseta.limpiar()
        for label_error in self.labels_error:
            label_error.config(text="")

    def al_cerrar(self):
        if messagebox.askyesno("Salir", "¿Seguro que quieres cerrar la aplicación?"):
            self.ventana_principal.destroy()

    def crear_campo(self, texto, variable, validacion):
        label = tk.Label(self.ventana_principal, text=texto, bg=FONDO)
        entry = tk.Entry(self.ventana_principal, textvariable=variable)
        label_error = tk.Label(self.ventana_principal, text="", fg=ROJO, bg=FONDO)
        entry.bind(
            "<KeyRelease>",
            lambda evento: self.al_soltar_tecla(validacion, label_error)
        )

        label.pack()
        entry.pack()
        label_error.pack()
        self.labels_error.append(label_error)

    def mostrar_interfaz(self):
        camiseta = self.camiseta
        self.ventana_principal.title("Camisetas")
        self.ventana_principal.geometry("300x500")

        self.crear_campo(
            "Color de la camiseta", camiseta.color,
            lambda: Validaciones.validarLetras(camiseta.color.get(), "Color", 30),
        )
        self.crear_campo(
            "Marca de la camiseta", camiseta.marca,
            lambda: Validaciones.validarTexto(camiseta.marca.get(), "Marca", 30),
        )

        label_talla = tk.Label(self.ventana_principal, text="Talla de la camiseta", bg=FONDO)
        combo_talla = ttk.Combobox(
            self.ventana_principal,
            textvariable=camiseta.talla,
            values=["S", "M", "L", "XL"],
            state="readonly",
        )

        label_fecha = tk.Label(self.ventana_principal, text="Fecha de creación", bg=FONDO)
        fecha = DateEntry(
            self.ventana_principal,
            textvariable=camiseta.fecha_creacion,
            date_pattern="dd/mm/yyyy",
        )

        label_material = tk.Label(self.ventana_principal, text="Material de la camiseta", bg=FONDO)
        radio_algodon = tk.Radiobutton(
            self.ventana_principal, text="Algodón", variable=camiseta.material,
            value="Algodón", bg=FONDO,
        )
        radio_poliester = tk.Radiobutton(
            self.ventana_principal, text="Poliéster", variable=camiseta.material,
            value="Poliéster", bg=FONDO,
        )
        radio_lana = tk.Radiobutton(
            self.ventana_principal, text="Lana", variable=camiseta.material,
            value="Lana", bg=FONDO,
        )

        boton_guardar = tk.Button(self.ventana_principal, text="Guardar", command=self.accion_guardar)
        boton_limpiar = tk.Button(self.ventana_principal, text="Limpiar", command=self.accion_limpiar)

        label_talla.pack()
        combo_talla.pack()

        label_fecha.pack()
        fecha.pack()

        label_material.pack()
        radio_algodon.pack()
        radio_poliester.pack()
        radio_lana.pack()

        boton_guardar.pack(pady=5)
        boton_limpiar.pack()

        self.ventana_principal.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        self.ventana_principal.mainloop()