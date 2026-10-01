import tkinter as tk
import re

texto_validar_nombre = ""

ventanaPrincipal = tk .Tk()
nombre = tk.StringVar(ventanaPrincipal)
labelNombre = tk.Label(ventanaPrincipal, text ="Nombre")
entryNombre = tk.Entry(ventanaPrincipal, textvariable=nombre)
labelValidacionNombre = tk.Label(ventanaPrincipal, text="")


def validarLetras(valor):
    patron = re._compile("^[A-Za-zñÑ ]*$")
    resultado = patron.match(valor.get()) is not None
    if not resultado:
        return False
    return True

def evento_presionar_tecla(evento):
    global texto_validar_nombre
    global nombre
    if validarLetras(nombre):
        texto_validar_nombre = ""

    else:
        texto_validar_nombre = "Solo se permite Letras"
    labelValidacionNombre.config(text = texto_validar_nombre)

#creando la ventana
ventanaPrincipal.title("Ventana Principal")
ventanaPrincipal.geometry("300x300")
labelNombre.pack()
entryNombre.bind("<KeyRelease>", evento_presionar_tecla)
entryNombre.pack()
labelValidacionNombre.pack()


ventanaPrincipal.mainloop()