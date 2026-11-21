import re
from decimal import Decimal, InvalidOperation


class Validaciones():

    @staticmethod
    def validarTexto(valor, campo, maximo):
        texto = valor.strip()
        if not texto:
            return campo + ': falta este dato.'
        if len(texto) > maximo:
            return campo + ': admite máximo ' + str(maximo) + ' caracteres.'
        return None

    @staticmethod
    def validarEntero(valor, campo, minimo, maximo):
        texto = valor.strip()
        if not re.fullmatch('[0-9]+', texto) or not minimo <= int(texto) <= maximo:
            return campo + ': debe ser un entero entre ' + str(minimo) + ' y ' + str(maximo) + '.'
        return None

    @staticmethod
    def validarPrecio(valor, campo):
        texto = valor.strip().replace(',', '.')
        try:
            numero = Decimal(texto)
        except InvalidOperation:
            return campo + ': debe ser un número.'
        if not numero.is_finite():
            return campo + ': debe ser un número.'
        if numero <= 0:
            return campo + ': debe ser mayor que cero.'
        if numero > Decimal('99999999.99'):
            return campo + ': el valor es demasiado grande.'
        if numero.as_tuple().exponent < -2:
            return campo + ': admite máximo 2 decimales.'
        return None

    @staticmethod
    def validarOpcion(valor, campo, opciones):
        if valor not in opciones:
            return campo + ': elija una opción de la lista.'
        return None

    @staticmethod
    def validarProducto(producto):
        errores = [
            Validaciones.validarTexto(producto.nombre.get(), 'Nombre', 100),
            Validaciones.validarPrecio(producto.precio.get(), 'Precio'),
            Validaciones.validarEntero(producto.stock.get() or '0', 'Stock', 0, 1000000),
        ]
        return [error for error in errores if error]

    @staticmethod
    def validarVenta(venta, metodos):
        errores = [
            Validaciones.validarTexto(venta.cliente.get(), 'Cliente', 100),
            Validaciones.validarOpcion(venta.metodo_pago.get(), 'Pago', metodos),
        ]
        return [error for error in errores if error]

    @staticmethod
    def validarDetalle(hay_producto, cantidad, stock):
        if not hay_producto:
            return ['Producto: elija uno de la lista.']
        error = Validaciones.validarEntero(cantidad, 'Cantidad', 1, max(stock, 1))
        if error:
            return [error]
        return []