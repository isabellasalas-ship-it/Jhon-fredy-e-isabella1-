import tkinter as tk
from tkinter import messagebox, ttk

from controladores.comunicacion import ErrorComunicacion


class VistaBase(ttk.Frame):

    titulo_formulario = ''
    recurso = ''
    columnas = ()

    def __init__(self, contenedor, comunicacion):
        super().__init__(contenedor, padding=10)
        self.comunicacion = comunicacion
        self.modelo = self.crear_modelo()
        self.registros = {}

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.crear_formulario()
        self.crear_botones()
        self.crear_tabla()
        self.crear_estado()

    def crear_modelo(self):
        raise NotImplementedError

    def crear_campos(self, marco):
        raise NotImplementedError

    def crear_botones_extra(self, marco):
        pass

    def validar(self):
        raise NotImplementedError

    def datos_formulario(self):
        raise NotImplementedError

    def valores_fila(self, registro):
        raise NotImplementedError

    def texto_confirmar_eliminar(self, registro):
        raise NotImplementedError

    def crear_formulario(self):
        marco = ttk.LabelFrame(self, text=self.titulo_formulario, padding=10)
        marco.grid(row=0, column=0, sticky='ew')
        marco.columnconfigure(1, weight=1)
        marco.columnconfigure(3, weight=1)
        self.crear_campos(marco)

    def agregar_campo(self, marco, fila, columna, texto, campo):
        etiqueta = ttk.Label(marco, text=texto)
        etiqueta.grid(row=fila, column=columna, sticky='w', padx=(0, 6), pady=4)
        campo.grid(row=fila, column=columna + 1, sticky='ew', padx=(0, 16), pady=4)

    def crear_botones(self):
        marco = ttk.Frame(self)
        marco.grid(row=1, column=0, sticky='ew', pady=8)

        self.boton_guardar = ttk.Button(marco, text='Guardar', command=self.accion_guardar)
        self.boton_eliminar = ttk.Button(marco, text='Eliminar', command=self.accion_eliminar)
        boton_limpiar = ttk.Button(marco, text='Limpiar', command=self.accion_limpiar)
        boton_consultar = ttk.Button(marco, text='Consultar', command=self.refrescar)

        self.boton_guardar.pack(side='left')
        self.boton_eliminar.pack(side='left', padx=8)
        boton_limpiar.pack(side='left')
        boton_consultar.pack(side='left', padx=8)

        self.crear_botones_extra(marco)
        self.actualizar_botones()

    def crear_tabla(self):
        marco = ttk.Frame(self)
        marco.grid(row=2, column=0, sticky='nsew')
        marco.columnconfigure(0, weight=1)
        marco.rowconfigure(0, weight=1)

        claves = [columna[0] for columna in self.columnas]
        self.tabla = ttk.Treeview(marco, columns=claves, show='headings', selectmode='browse')
        for clave, titulo, ancho in self.columnas:
            self.tabla.heading(clave, text=titulo, anchor='w')
            self.tabla.column(clave, width=ancho, anchor='w')

        barra = ttk.Scrollbar(marco, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)

        self.tabla.grid(row=0, column=0, sticky='nsew')
        barra.grid(row=0, column=1, sticky='ns')

        self.tabla.bind('<<TreeviewSelect>>', self.al_seleccionar)

    def crear_estado(self):
        self.estado = tk.StringVar(self)
        etiqueta = ttk.Label(self, textvariable=self.estado, foreground='green')
        etiqueta.grid(row=3, column=0, sticky='w', pady=(8, 0))

    def mostrar_estado(self, mensaje):
        self.estado.set(mensaje)

    def refrescar(self, mensaje=''):
        try:
            datos = self.consultar_registros()
        except ErrorComunicacion as error:
            messagebox.showerror('No se pudo consultar', str(error))
            return
        self.mostrar_registros(datos)
        self.mostrar_estado(mensaje)

    def consultar_registros(self):
        return self.comunicacion.listar(self.recurso)

    def mostrar_registros(self, registros):
        self.tabla.delete(*self.tabla.get_children())
        self.registros = {registro['id']: registro for registro in registros}
        for registro in registros:
            self.tabla.insert('', 'end', iid=str(registro['id']), values=self.valores_fila(registro))

        if self.modelo.id in self.registros:
            self.modelo.cargar(self.registros[self.modelo.id])
            self.tabla.selection_set(str(self.modelo.id))
            self.actualizar_botones()
        elif self.modelo.id is not None:
            self.accion_limpiar()

    def al_seleccionar(self, evento):
        seleccion = self.tabla.selection()
        if not seleccion or int(seleccion[0]) == self.modelo.id:
            return
        self.modelo.cargar(self.registros[int(seleccion[0])])
        self.actualizar_botones()
        self.mostrar_estado('')

    def accion_limpiar(self):
        self.modelo.limpiar()
        self.tabla.selection_remove(*self.tabla.selection())
        self.actualizar_botones()
        self.mostrar_estado('')

    def actualizar_botones(self):
        editando = self.modelo.id is not None
        self.boton_guardar.config(text='Actualizar' if editando else 'Guardar')
        self.boton_eliminar.state(['!disabled'] if editando else ['disabled'])

    def accion_guardar(self):
        errores = self.validar()
        if errores:
            messagebox.showwarning('Revise los datos', '\n'.join(errores))
            return

        id = self.modelo.id
        datos = self.datos_formulario()
        try:
            if id is None:
                self.comunicacion.crear(self.recurso, datos)
            else:
                self.comunicacion.reemplazar(self.recurso, id, datos)
        except ErrorComunicacion as error:
            messagebox.showerror('No se pudo guardar', str(error))
            return

        self.accion_limpiar()
        self.refrescar('Registro guardado.' if id is None else 'Registro actualizado.')

    def accion_eliminar(self):
        registro = self.registros.get(self.modelo.id)
        if registro is None:
            return
        if not messagebox.askyesno('Confirmar', self.texto_confirmar_eliminar(registro)):
            return

        try:
            self.comunicacion.eliminar(self.recurso, registro['id'])
        except ErrorComunicacion as error:
            messagebox.showerror('No se pudo eliminar', str(error))
            return

        self.accion_limpiar()
        self.refrescar('Registro eliminado.')