from tkinter import ttk

from vistas import tema


def aplicar_estilos(ventana):
    estilo = ttk.Style(ventana)
    estilo.theme_use('clam')

    estilo.configure('TNotebook', background=tema.COLOR_FONDO, borderwidth=0)
    estilo.configure('TNotebook.Tab', background=tema.COLOR_MARCO, foreground=tema.COLOR_TEXTO, font=tema.FUENTE_NEGRITA, padding=(24, 8), borderwidth=0, focuscolor=tema.COLOR_BOTON)
    estilo.map('TNotebook.Tab', background=[('selected', tema.COLOR_BOTON)], foreground=[('selected', tema.COLOR_BLANCO)], padding=[('selected', (30, 13))])
    estilo.configure('Marco.TFrame', background=tema.COLOR_MARCO)

    estilo.configure('Treeview', background=tema.COLOR_BLANCO, fieldbackground=tema.COLOR_BLANCO, foreground=tema.COLOR_TEXTO, font=tema.FUENTE_NORMAL, rowheight=30, borderwidth=0)
    estilo.map('Treeview', background=[('selected', tema.COLOR_BOTON)], foreground=[('selected', tema.COLOR_BLANCO)])
    estilo.configure('Treeview.Heading', background=tema.COLOR_BOTON, foreground=tema.COLOR_TEXTO, font=tema.FUENTE_NEGRITA, padding=6, relief='flat')
    estilo.map('Treeview.Heading', background=[('active', tema.COLOR_BOTON_HOVER)])

    estilo.configure('Redondo.TCombobox', fieldbackground=tema.COLOR_BLANCO, background=tema.COLOR_BOTON, foreground=tema.COLOR_TEXTO, arrowcolor=tema.COLOR_TEXTO, bordercolor=tema.COLOR_BLANCO, lightcolor=tema.COLOR_BLANCO, darkcolor=tema.COLOR_BLANCO, borderwidth=0, padding=4)
    estilo.map('Redondo.TCombobox', fieldbackground=[('readonly', tema.COLOR_BLANCO)], selectbackground=[('readonly', tema.COLOR_BLANCO)], selectforeground=[('readonly', tema.COLOR_TEXTO)])
    ventana.option_add('*TCombobox*Listbox.font', tema.FUENTE_NORMAL)
    ventana.option_add('*TCombobox*Listbox.background', tema.COLOR_BLANCO)
    ventana.option_add('*TCombobox*Listbox.foreground', tema.COLOR_TEXTO)
    ventana.option_add('*TCombobox*Listbox.selectBackground', tema.COLOR_BOTON)
    ventana.option_add('*TCombobox*Listbox.selectForeground', tema.COLOR_BLANCO)

    estilo.configure('Cafe.Horizontal.TProgressbar', troughcolor=tema.COLOR_FONDO, background=tema.COLOR_BOTON, bordercolor=tema.COLOR_MARCO, lightcolor=tema.COLOR_BOTON, darkcolor=tema.COLOR_BOTON)