import tkinter as tk
from tkinter import ttk, messagebox

from vistas import tema
from vistas.widgets import BotonRedondo


class VistaBase(ttk.Frame):
    """CRUD completo: formulario, botones y tabla.

    Cada pestaña hereda de esta clase y solo escribe lo que es suyo.
    """

    recurso = ''
    columnas = ()                    
    texto_guardar = '＋ Guardar nuevo'
    texto_eliminar = '🗑 Eliminar'
    conservar_seleccion = False

    def __init__(self, contenedor, interfaz):
        super().__init__(contenedor, style='Marco.TFrame')
        self.interfaz = interfaz
        self.comunicacion = interfaz.comunicacion
        self.modelo = self.crear_modelo()
        self.registros = {}
        self.botones = []
        self.ocupado = False

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.principal = tk.Frame(self, bg=tema.COLOR_MARCO)
        self.principal.grid(row=0, column=0, sticky='nsew', padx=15, pady=12)

        self.crear_formulario()
        self.crear_barra_extra()
        self.crear_tabla()
        self.crear_panel_extra()
        self.actualizar_botones()

    
    def crear_modelo(self):
        raise NotImplementedError

    def crear_campos(self, marco):
        raise NotImplementedError

    def valores_fila(self, registro):
        raise NotImplementedError

    def crear_botones_extra(self, marco):
        pass

    def crear_barra_extra(self):
        pass

    def crear_panel_extra(self):
        pass

    def configurar_tabla(self):
        pass

    def validar(self):
        return []

    def datos_formulario(self):
        return self.modelo.a_diccionario()

    def etiqueta_fila(self, registro):
        return ''

    def mostrar_fila(self, registro):
        return True

    def al_limpiar(self):
        pass

    def texto_confirmar_eliminar(self, registro):
        return '¿Seguro que quieres eliminar este registro?'

    
    def boton(self, padre, texto, comando, color):
        boton = BotonRedondo(padre, texto, comando, color=color, fondo=tema.COLOR_MARCO)
        self.botones.append(boton)
        return boton

    def crear_formulario(self):
        campos = tk.Frame(self.principal, bg=tema.COLOR_MARCO)
        campos.pack(fill='x')
        self.crear_campos(campos)

        botones = tk.Frame(self.principal, bg=tema.COLOR_MARCO)
        botones.pack(fill='x', pady=8)
        self.btn_guardar = self.boton(botones, self.texto_guardar, self.accion_guardar, tema.COLOR_VERDE)
        self.btn_actualizar = self.boton(botones, '✎ Actualizar', self.accion_actualizar, tema.COLOR_BOTON)
        self.btn_eliminar = self.boton(botones, self.texto_eliminar, self.accion_eliminar, tema.COLOR_ALERTA)
        self.btn_limpiar = self.boton(botones, '✕ Limpiar', self.accion_limpiar, tema.COLOR_FONDO)
        for boton in (self.btn_guardar, self.btn_actualizar, self.btn_eliminar, self.btn_limpiar):
            boton.pack(side='left', padx=(0, 8))
        self.crear_botones_extra(botones)

    def crear_tabla(self):
        contenedor = tk.Frame(self.principal, bg=tema.COLOR_MARCO)
        contenedor.pack(fill='both', expand=True)

        claves = [columna[0] for columna in self.columnas]
        self.tabla = ttk.Treeview(
            contenedor, columns=claves, show='headings', selectmode='browse', height=6
        )
        for clave, titulo, ancho, alineacion in self.columnas:
            self.tabla.heading(clave, text=titulo)
            self.tabla.column(clave, width=ancho, anchor=alineacion)
        self.configurar_tabla()

        barra = ttk.Scrollbar(contenedor, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        self.tabla.pack(side='left', fill='both', expand=True)
        barra.pack(side='right', fill='y')

        
        self.tabla.bind('<<TreeviewSelect>>', self.al_seleccionar)
        self.tabla.bind('<Delete>', lambda evento: self.accion_eliminar())

    
    def bloquear(self, bloquear):
        self.ocupado = bloquear
        self.actualizar_botones()

    def actualizar_botones(self):
        editando = self.modelo.id is not None
        for boton in self.botones:
            boton.activar(not self.ocupado)
        if not self.ocupado:
            self.btn_actualizar.activar(editando)
            self.btn_eliminar.activar(editando)

    
    def refrescar(self, manual=False):
        self.bloquear(True)
        self.interfaz.ejecutar(
            self.consultar_registros, self.al_consultar, self.al_fallar,
            mensaje='Cargando...', minimo=tema.PAUSA_ACCION if manual else 0.0,
        )

    def consultar_registros(self):
        return self.comunicacion.listar(self.recurso)

    def al_consultar(self, datos):
        self.bloquear(False)
        self.mostrar_registros(datos)

    def al_fallar(self, error):
        self.bloquear(False)
        self.interfaz.mostrar_error(error)

    def mostrar_registros(self, registros):
        self.registros = {registro['id']: registro for registro in registros}
        self.pintar_tabla()

        if self.modelo.id in self.registros:
            self.modelo.cargar(self.registros[self.modelo.id])
            if self.tabla.exists(str(self.modelo.id)):
                self.tabla.selection_set(str(self.modelo.id))
        elif self.modelo.id is not None:
            self.accion_limpiar()
        self.actualizar_botones()

    def pintar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for registro in self.registros.values():
            if not self.mostrar_fila(registro):
                continue
            self.tabla.insert(
                '', 'end', iid=str(registro['id']),
                values=self.valores_fila(registro),
                tags=(self.etiqueta_fila(registro),),
            )

    
    def al_seleccionar(self, evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        id_registro = int(seleccion[0])
        if id_registro == self.modelo.id:
            return
        self.modelo.cargar(self.registros[id_registro])
        self.actualizar_botones()

    def accion_limpiar(self):
        self.modelo.limpiar()
        self.tabla.selection_remove(self.tabla.selection())
        self.al_limpiar()
        self.actualizar_botones()

    def ejecutar_accion(self, funcion, carga, exito):
        self.bloquear(True)

        def al_terminar(resultado):
            if self.conservar_seleccion and isinstance(resultado, dict):
                self.modelo.id = resultado['id']
            else:
                self.accion_limpiar()
            self.refrescar()
            messagebox.showinfo('Listo', exito)

        self.interfaz.ejecutar(
            funcion, al_terminar, self.al_fallar,
            mensaje=carga, minimo=tema.PAUSA_ACCION,
        )

    def accion_guardar(self):                                  
        errores = self.validar()
        if errores:
            messagebox.showwarning('Revise los datos', '\n'.join(errores))
            return
        datos = self.datos_formulario()
        self.ejecutar_accion(
            lambda: self.comunicacion.crear(self.recurso, datos),
            'Guardando...', 'Guardado correctamente.',
        )

    def accion_actualizar(self):                              
        if self.modelo.id is None:
            messagebox.showinfo('Elige un registro', 'Primero selecciona uno de la tabla.')
            return
        errores = self.validar()
        if errores:
            messagebox.showwarning('Revise los datos', '\n'.join(errores))
            return
        id_registro = self.modelo.id
        datos = self.datos_formulario()
        self.ejecutar_accion(
            lambda: self.comunicacion.reemplazar(self.recurso, id_registro, datos),
            'Actualizando...', 'Actualizado correctamente.',
        )

    def accion_eliminar(self):                                
        registro = self.registros.get(self.modelo.id)
        if registro is None:
            messagebox.showinfo('Elige un registro', 'Primero selecciona uno de la tabla.')
            return
        if not messagebox.askyesno('Confirmar', self.texto_confirmar_eliminar(registro)):
            return
        id_registro = registro['id']
        self.ejecutar_accion(
            lambda: self.comunicacion.eliminar(self.recurso, id_registro),
            'Eliminando...', 'Eliminado correctamente.',
        )