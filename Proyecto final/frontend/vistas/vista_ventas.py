import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

from controladores.validaciones import Validaciones
from modelos.detalle import Detalle
from modelos.venta import Venta
from vistas import tema
from vistas.vista_base import VistaBase
from vistas.widgets import combo_redondo, entrada_redonda

TEXTO_NUEVA = 'Venta nueva: escribe el cliente y agrega productos'


def dinero(valor):
    numero = float(valor)
    if numero.is_integer():
        return f'${numero:,.0f}'
    return f'${numero:,.2f}'


def formato_fecha(texto):
    try:
        return datetime.fromisoformat(texto).astimezone().strftime('%d/%m/%Y %H:%M')
    except ValueError:
        return texto


class VistaVentas(VistaBase):

    recurso = 'ventas'
    texto_guardar = '＋ Crear venta'
    texto_eliminar = '🗑 Eliminar venta'
    conservar_seleccion = True
    columnas = (
        ('id', 'N°', 40, 'center'),
        ('fecha', 'Fecha', 120, 'center'),
        ('cliente', 'Cliente', 130, 'w'),
        ('total', 'Total', 90, 'e'),
    )

    def crear_modelo(self):
        self.detalle = Detalle(self)
        self.productos = []
        self.detalles = []
        self.opciones = []
        return Venta(self)

    def etiqueta(self, padre, texto):
        return tk.Label(
            padre, text=texto, font=tema.FUENTE_NORMAL,
            bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO,
        )

    
    def crear_campos(self, marco):
        marco.columnconfigure(1, weight=1)
        tk.Label(
            marco, text='1. Venta', font=tema.FUENTE_NEGRITA,
            bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO,
        ).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 6))

        self.etiqueta(marco, 'Cliente:').grid(row=1, column=0, sticky='e', pady=4)
        self.entrada_cliente = entrada_redonda(marco, self.modelo.cliente)
        self.entrada_cliente.grid(row=1, column=1, sticky='ew', padx=6, pady=4)
        self.entrada_cliente.hijo.bind('<Return>', lambda evento: self.accion_guardar())

        self.etiqueta(marco, 'Pago:').grid(row=2, column=0, sticky='e', pady=4)
        self.combo_pago = combo_redondo(
            marco, self.modelo.metodo_pago, valores=list(Venta.METODOS)
        )
        self.combo_pago.grid(row=2, column=1, sticky='ew', padx=6, pady=4)

        self.etiqueta(marco, 'Notas:').grid(row=3, column=0, sticky='e', pady=4)
        entrada_redonda(marco, self.modelo.observaciones).grid(
            row=3, column=1, sticky='ew', padx=6, pady=4
        )

    def crear_barra_extra(self):
        tk.Label(
            self.principal,
            text='Tip: sin venta elegida, al agregar un producto la venta se crea sola. '
                 'Usa Limpiar para empezar otra.',
            font=tema.FUENTE_PEQUENA, bg=tema.COLOR_MARCO, fg=tema.COLOR_GRIS,
            anchor='w', justify='left', wraplength=420,
        ).pack(fill='x', pady=(0, 8))

    
    def crear_panel_extra(self):
        self.columnconfigure(1, weight=1)
        panel = tk.Frame(self, bg=tema.COLOR_MARCO)
        panel.grid(row=0, column=1, sticky='nsew', padx=(0, 15), pady=12)

        tk.Label(
            panel, text='2. Productos de la venta', font=tema.FUENTE_NEGRITA,
            bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO,
        ).pack(anchor='w', pady=(0, 6))

        self.lbl_venta = tk.Label(
            panel, text=TEXTO_NUEVA, font=tema.FUENTE_PEQUENA,
            bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO, anchor='w',
        )
        self.lbl_venta.pack(fill='x', pady=(0, 4))

        self.combo_producto = combo_redondo(panel, self.detalle.producto)
        self.combo_producto.pack(fill='x')

        fila = tk.Frame(panel, bg=tema.COLOR_MARCO)
        fila.pack(fill='x', pady=8)
        self.etiqueta(fila, 'Cantidad:').pack(side='left')
        caja = entrada_redonda(fila, self.detalle.cantidad, ancho=70)
        caja.pack(side='left', padx=6)
        caja.hijo.bind('<Return>', lambda evento: self.accion_agregar())
        self.boton(fila, '＋ Agregar', self.accion_agregar, tema.COLOR_VERDE).pack(side='left', padx=4)
        self.boton(fila, '− Quitar', self.accion_quitar, tema.COLOR_NARANJA).pack(side='left', padx=4)

        contenedor = tk.Frame(panel, bg=tema.COLOR_MARCO)
        contenedor.pack(fill='both', expand=True)
        self.tabla_det = ttk.Treeview(
            contenedor, columns=('producto', 'cantidad', 'precio', 'subtotal'),
            show='headings', selectmode='browse', height=6,
        )
        self.tabla_det.heading('producto', text='Producto')
        self.tabla_det.heading('cantidad', text='Cant.')
        self.tabla_det.heading('precio', text='Precio')
        self.tabla_det.heading('subtotal', text='Subtotal')
        self.tabla_det.column('producto', width=130, anchor='w')
        self.tabla_det.column('cantidad', width=50, anchor='center')
        self.tabla_det.column('precio', width=80, anchor='e')
        self.tabla_det.column('subtotal', width=90, anchor='e')

        barra = ttk.Scrollbar(contenedor, orient='vertical', command=self.tabla_det.yview)
        self.tabla_det.configure(yscrollcommand=barra.set)
        self.tabla_det.pack(side='left', fill='both', expand=True)
        barra.pack(side='right', fill='y')

        self.lbl_total = tk.Label(
            panel, text='Total: $0', font=('Segoe UI', 18, 'bold'),
            bg=tema.COLOR_MARCO, fg=tema.COLOR_TEXTO, anchor='e',
        )
        self.lbl_total.pack(fill='x', pady=(8, 0))

    
    def consultar_registros(self):
        id_venta = self.modelo.id
        datos = {
            'ventas': self.comunicacion.listar('ventas'),
            'productos': self.comunicacion.listar('productos'),
            'detalles': [],
        }
        if id_venta is not None:
            datos['detalles'] = self.comunicacion.listar('detalles', {'venta': id_venta})
        return datos

    def mostrar_registros(self, datos):
        self.productos = datos['productos']
        self.detalles = datos['detalles']
        super().mostrar_registros(datos['ventas'])
        self.mostrar_detalles()
        self.llenar_combo()

    def cargar_detalles(self):
        id_venta = self.modelo.id
        self.interfaz.ejecutar(
            lambda: self.comunicacion.listar('detalles', {'venta': id_venta}),
            self.al_cargar_detalles, self.al_fallar,
            mensaje='Cargando productos de la venta...',
        )

    def al_cargar_detalles(self, detalles):
        self.detalles = detalles
        self.mostrar_detalles()

    def mostrar_detalles(self):
        self.tabla_det.delete(*self.tabla_det.get_children())
        nombres = {producto['id']: producto['nombre'] for producto in self.productos}
        for d in self.detalles:
            subtotal = d['cantidad'] * float(d['precio_unitario'])
            self.tabla_det.insert(
                '', 'end', iid=str(d['id']),
                values=(nombres.get(d['producto'], 'Producto ' + str(d['producto'])),
                        d['cantidad'], dinero(d['precio_unitario']), dinero(subtotal)),
            )

        venta = self.registros.get(self.modelo.id)
        if venta is None:
            self.lbl_venta.config(text=TEXTO_NUEVA)
            self.lbl_total.config(text='Total: $0')
        else:
            self.lbl_venta.config(text='Venta N° ' + str(venta['id']) + '  ·  ' + venta['cliente'])
            self.lbl_total.config(text='Total: ' + dinero(venta['total']))

    def llenar_combo(self):
        
        self.opciones = [p for p in self.productos if p['activo'] and p['stock'] > 0]
        textos = []
        for p in self.opciones:
            textos.append(p['nombre'] + '  —  ' + dinero(p['precio']) + '  (quedan ' + str(p['stock']) + ')')
        self.combo_producto.hijo['values'] = textos
        self.detalle.producto.set('')

    
    def al_seleccionar(self, evento):
        anterior = self.modelo.id
        super().al_seleccionar(evento)
        if self.modelo.id is not None and self.modelo.id != anterior:
            self.cargar_detalles()

    def al_limpiar(self):
        self.detalles = []
        self.detalle.limpiar()
        self.mostrar_detalles()
        self.entrada_cliente.hijo.focus_set()

    
    def validar(self):
        return Validaciones.validarVenta(self.modelo, list(Venta.METODOS))

    def valores_fila(self, registro):
        return (
            registro['id'],
            formato_fecha(registro['fecha']),
            registro['cliente'],
            dinero(registro['total']),
        )

    def texto_confirmar_eliminar(self, registro):
        return '¿Seguro que quieres eliminar la venta N° ' + str(registro['id']) + '?'

    
    def accion_agregar(self):
        id_venta = self.modelo.id
        if id_venta is None:
            errores = self.validar()
            if errores:
                messagebox.showwarning('Revise los datos', '\n'.join(errores))
                return

        indice = self.combo_producto.hijo.current()
        producto = self.opciones[indice] if indice >= 0 else None
        stock = producto['stock'] if producto else 0
        errores = Validaciones.validarDetalle(
            producto is not None, self.detalle.cantidad.get(), stock
        )
        if errores:
            messagebox.showwarning('Revise los datos', '\n'.join(errores))
            return

        datos_venta = self.modelo.a_diccionario() if id_venta is None else None
        datos_detalle = self.detalle.a_diccionario(id_venta, producto['id'])
        estado = {'id': id_venta, 'creada': False}

        def trabajo():
            
            if estado['id'] is None:
                venta = self.comunicacion.crear('ventas', datos_venta)
                estado['id'] = venta['id']
                estado['creada'] = True
            datos_detalle['venta'] = estado['id']
            return self.comunicacion.crear('detalles', datos_detalle)

        def al_terminar(_resultado):
            self.modelo.id = estado['id']
            self.detalle.limpiar()
            self.refrescar()

        def al_fallar(error):
            if estado['creada']:
                self.modelo.id = estado['id']
                self.refrescar()
            else:
                self.bloquear(False)
            self.interfaz.mostrar_error(error)

        self.bloquear(True)
        self.interfaz.ejecutar(
            trabajo, al_terminar, al_fallar,
            mensaje='Agregando producto...', minimo=tema.PAUSA_ACCION,
        )

    def accion_quitar(self):
        seleccion = self.tabla_det.selection()
        if not seleccion:
            messagebox.showinfo('Elige un producto', 'Selecciona en la tabla el producto que quieres quitar.')
            return
        id_detalle = int(seleccion[0])

        self.bloquear(True)
        self.interfaz.ejecutar(
            lambda: self.comunicacion.eliminar('detalles', id_detalle),
            lambda _resultado: self.refrescar(), self.al_fallar,
            mensaje='Quitando producto...', minimo=tema.PAUSA_ACCION,
        )