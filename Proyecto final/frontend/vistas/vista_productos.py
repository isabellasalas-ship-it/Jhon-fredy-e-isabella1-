import tkinter as tk

from modelos.producto import Producto
from controladores.validaciones import Validaciones
from vistas import tema
from vistas.vista_base import VistaBase
from vistas.widgets import entrada_redonda

STOCK_BAJO = 5


def formato_precio(valor):
    numero = float(valor)
    if numero.is_integer():
        return f'${numero:,.0f}'
    return f'${numero:,.2f}'


def estado_de(registro):
    if not registro['activo']:
        return 'inactivo', 'Inactivo'
    if registro['stock'] == 0:
        return 'agotado', 'Agotado'
    if registro['stock'] <= STOCK_BAJO:
        return 'bajo', 'Poco stock'
    return '', 'Activo'


class VistaProductos(VistaBase):

    recurso = 'productos'
    columnas = (
        ('id', 'ID', 60, 'center'),
        ('nombre', 'Nombre', 300, 'w'),
        ('precio', 'Precio', 120, 'e'),
        ('stock', 'Stock', 90, 'center'),
        ('estado', 'Estado', 110, 'center'),
    )

    def crear_modelo(self):
        return Producto(self)

    def crear_campos(self, marco):
        campos = [
            ('Nombre:', self.modelo.nombre, 0, 260),
            ('Precio:', self.modelo.precio, 2, 130),
            ('Stock:', self.modelo.stock, 4, 90),
        ]
        for texto, variable, columna, ancho in campos:
            tk.Label(
                marco, text=texto, font=tema.FUENTE_NORMAL,
                bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO,
            ).grid(row=0, column=columna, padx=(10, 4), pady=6, sticky='e')
            caja = entrada_redonda(marco, variable, ancho=ancho)
            caja.grid(row=0, column=columna + 1, padx=(0, 10), pady=6)
            caja.hijo.bind('<Return>', lambda evento: self.accion_guardar())
            if columna == 0:
                self.entrada_nombre = caja

        tk.Checkbutton(
            marco, text='Activo', variable=self.modelo.activo,
            font=tema.FUENTE_NORMAL, bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO,
            activebackground=tema.COLOR_MARCO, selectcolor=tema.COLOR_BLANCO,
        ).grid(row=0, column=6, padx=10)

    def crear_botones_extra(self, marco):
        self.btn_estado = self.boton(
            marco, '⇄ Activar / Desactivar', self.accion_cambiar_estado, tema.COLOR_NARANJA
        )
        self.btn_estado.pack(side='left')

    def crear_barra_extra(self):
        barra = tk.Frame(self.principal, bg=tema.COLOR_MARCO)
        barra.pack(fill='x', pady=(0, 8))

        tk.Label(
            barra, text='Buscar:', font=tema.FUENTE_NORMAL,
            bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO,
        ).pack(side='left', padx=(10, 4))

        self.texto_busqueda = tk.StringVar(self)
        self.texto_busqueda.trace_add('write', lambda *args: self.pintar_tabla())
        entrada_redonda(barra, self.texto_busqueda, ancho=260).pack(side='left', padx=6)

        self.boton(
            barra, '↻ Recargar', lambda: self.refrescar(True), tema.COLOR_BOTON
        ).pack(side='right')

    def configurar_tabla(self):
        self.tabla.tag_configure('bajo', background=tema.COLOR_NARANJA)
        self.tabla.tag_configure('agotado', background=tema.COLOR_ALERTA)
        self.tabla.tag_configure('inactivo', foreground=tema.COLOR_GRIS)

    def actualizar_botones(self):
        super().actualizar_botones()
        if not self.ocupado:
            self.btn_estado.activar(self.modelo.id is not None)

    def al_limpiar(self):
        self.entrada_nombre.hijo.focus_set()

    def validar(self):
        return Validaciones.validarProducto(self.modelo)

    def mostrar_fila(self, registro):
        filtro = self.texto_busqueda.get().strip().lower()
        return not filtro or filtro in registro['nombre'].lower()

    def etiqueta_fila(self, registro):
        return estado_de(registro)[0]

    def valores_fila(self, registro):
        return (
            registro['id'],
            registro['nombre'],
            formato_precio(registro['precio']),
            registro['stock'],
            estado_de(registro)[1],
        )

    def texto_confirmar_eliminar(self, registro):
        return '¿Seguro que quieres eliminar «' + registro['nombre'] + '»?'

    def accion_cambiar_estado(self):                          
        registro = self.registros.get(self.modelo.id)
        if registro is None:
            return
        nuevo = not registro['activo']
        if nuevo:
            mensaje = 'Producto activado.'
        else:
            mensaje = 'Producto desactivado (su historial se conserva).'
        id_registro = registro['id']
        self.ejecutar_accion(
            lambda: self.comunicacion.modificar(self.recurso, id_registro, {'activo': nuevo}),
            'Cambiando estado...', mensaje,
        )