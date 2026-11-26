import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from controladores.comunicacion import Comunicacion
from vistas.vista_camisetas import VistaCamisetas

FONDO = "#f3e5f5"
BOTON_ROSA = "#f48fb1"
BOTON_HOVER = "#f06292"


class Interfaz():

    def __init__(self):
        self.ventana_principal = tk.Tk()
        self.ventana_principal.configure(bg="#d6eaf8")# PROFE ESTO FUE OPCIONAL, SOLO PARA DARLE COLOR A LA VENTANA PRINCIPAL
        self.comunicacion = Comunicacion()
       

    def al_cambiar_pestana(self, evento):
        pestana = self.pestanas.nametowidget(self.pestanas.select())
        pestana.refrescar()
    
    def al_cerrar(self):
        if messagebox.askyesno('Salir', '¿Seguro que quieres cerrar la aplicación?'):
            self.ventana_principal.destroy()



    def mostrar_interfaz(self):
    
        self.ventana_principal.title("Camisetas")
        self.ventana_principal.geometry("900x600")
        self.ventana_principal.minsize(820, 520)

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TFrame", background=FONDO)
        estilo.configure("TLabelframe", background=FONDO)
        estilo.configure("TLabelframe.Label", background=FONDO)
        estilo.configure("TLabel", background=FONDO)
        estilo.configure("TRadiobutton", background=FONDO)
        estilo.configure("TNotebook", background=FONDO)
        estilo.configure("TNotebook.Tab", background="#e1bee7")  
        estilo.map("TNotebook.Tab", background=[("selected", FONDO)])
        estilo.configure("TButton", background=BOTON_ROSA, foreground="#2c2c2c")
        estilo.map("TButton", background=[("active", BOTON_HOVER), ("disabled", "#e0e0e0")])


        self.pestanas = ttk.Notebook(self.ventana_principal)
        self.pestanas.add(VistaCamisetas(self.pestanas, self.comunicacion), text='Camisetas')
        self.pestanas.pack(fill='both', expand=True)
        self.pestanas.bind('<<NotebookTabChanged>>', self.al_cambiar_pestana)

        
        """
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
        """

        self.ventana_principal.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        self.ventana_principal.mainloop()