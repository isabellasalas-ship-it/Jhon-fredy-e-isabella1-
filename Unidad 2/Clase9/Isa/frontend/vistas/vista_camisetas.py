from datetime import datetime
from tkinter import messagebox, ttk

from tkcalendar import DateEntry

from controladores.comunicacion import ErrorComunicacion
from controladores.validaciones import Validaciones
from modelos.camiseta import Camiseta
from vistas.vista_base import VistaBase


class VistaCamisetas(VistaBase):

    titulo_formulario = 'Datos de la camiseta'
    recurso = 'camisetas'
    columnas = (
        ('id', 'Id', 40),
        ('color', 'Color', 120),
        ('marca', 'Marca', 120),
        ('talla', 'Talla', 60),
        ('material', 'Material', 110),
        ('fecha_creacion', 'Fecha de creación', 130),
        ('activa', 'Activa', 60),
    )

    def crear_modelo(self):
        return Camiseta(self)

    def crear_campos(self, marco):
        entry_color = ttk.Entry(marco, textvariable=self.modelo.color)
        validacion_color = self.register(self.permitir_color)
        entry_color.config(validate='key', validatecommand=(validacion_color, '%P'))# lo volví a poner: en mi versión original el color solo dejaba escribir letras
        entry_marca = ttk.Entry(marco, textvariable=self.modelo.marca)
        combo_talla = ttk.Combobox(
            marco, textvariable=self.modelo.talla,
            values=['S', 'M', 'L', 'XL'], state='readonly',# la fecha solo se elige en el calendario, no se escribe
        )
        fecha = DateEntry(
            marco, textvariable=self.modelo.fecha_creacion,
            date_pattern='dd/mm/yyyy',state='readonly',
        )

        marco_material = ttk.Frame(marco)
        for material in ['Algodón', 'Poliéster', 'Lana']:
            radio = ttk.Radiobutton(
                marco_material, text=material,
                variable=self.modelo.material, value=material,
            )
            radio.pack(side='left', padx=(0, 10))

        self.agregar_campo(marco, 0, 0, 'Color', entry_color)
        self.agregar_campo(marco, 0, 2, 'Marca', entry_marca)
        self.agregar_campo(marco, 1, 0, 'Talla', combo_talla)
        self.agregar_campo(marco, 1, 2, 'Fecha de creación', fecha)
        self.agregar_campo(marco, 2, 0, 'Material', marco_material)
    def permitir_color(self, texto):
        return texto == '' or Validaciones.validarLetras(texto, 'Color', 30) is None

    def crear_botones_extra(self, marco):
        self.boton_estado = ttk.Button(marco, text='Desactivar', command=self.accion_cambiar_estado)
        self.boton_estado.pack(side='left', padx=(24, 0))

    def actualizar_botones(self):
        super().actualizar_botones()
        registro = self.registros.get(self.modelo.id)
        if registro is None:
            self.boton_estado.state(['disabled'])
        else:
            self.boton_estado.state(['!disabled'])
            self.boton_estado.config(text='Desactivar' if registro['activa'] else 'Activar')

    def accion_cambiar_estado(self):
        registro = self.registros[self.modelo.id]
        cambio = {'activa': not registro['activa']}
        try:
            self.comunicacion.modificar(self.recurso, registro['id'], cambio)
        except ErrorComunicacion as error:
            messagebox.showerror('No se pudo cambiar el estado', str(error))
            return
        self.refrescar('Camiseta activada.' if cambio['activa'] else 'Camiseta desactivada.')

    def validar(self):
        return Validaciones.validarCamiseta(self.modelo)

    def datos_formulario(self):
        return self.modelo.a_diccionario()

    def valores_fila(self, registro):
        fecha = datetime.strptime(registro['fecha_creacion'], '%Y-%m-%d').strftime('%d/%m/%Y')
        return (
            registro['id'],
            registro['color'],
            registro['marca'],
            registro['talla'],
            registro['material'],
            fecha,
            'Sí' if registro['activa'] else 'No',
        )

    def texto_confirmar_eliminar(self, registro):
        return '¿Eliminar la camiseta ' + registro['color'] + ' ' + registro['marca'] + '?'