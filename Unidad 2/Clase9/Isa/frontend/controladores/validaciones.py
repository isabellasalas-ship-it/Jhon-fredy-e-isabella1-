import re
from datetime import datetime, date


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
    def validarLetras(valor, campo, maximo):
        error = Validaciones.validarTexto(valor, campo, maximo)
        if error:
            return error
        if not re.fullmatch('[A-Za-zÁÉÍÓÚáéíóúÑñ ]+', valor.strip()):
            return campo + ': solo se permiten letras.'
        return None

    @staticmethod
    def validarOpcion(valor, campo, opciones):
        if valor not in opciones:
            return campo + ': seleccione ' + ', '.join(opciones) + '.'
        return None

    @staticmethod
    def validarFecha(valor, campo):
        try:
            datetime.strptime(valor.strip(), '%d/%m/%Y')
        except ValueError:
            return campo + ': use el formato DD/MM/AAAA.'
        return None

    @staticmethod
    def validarFechaNoFutura(valor, campo):
        try:
            fecha = datetime.strptime(valor.strip(), '%d/%m/%Y').date()
        except ValueError:
            return None
        if fecha > date.today():
            return campo + ': no puede ser una fecha futura.'
        return None

    @staticmethod
    def validarCamiseta(camiseta):
        errores = [
            Validaciones.validarLetras(camiseta.color.get(), 'Color', 30),
            Validaciones.validarTexto(camiseta.marca.get(), 'Marca', 30),
            Validaciones.validarOpcion(camiseta.talla.get(), 'Talla', ['S', 'M', 'L', 'XL']),
            Validaciones.validarFecha(camiseta.fecha_creacion.get(), 'Fecha de creación'),
            Validaciones.validarFechaNoFutura(camiseta.fecha_creacion.get(), 'Fecha de creación'),
            Validaciones.validarOpcion(camiseta.material.get(), 'Material', ['Algodón', 'Poliéster', 'Lana']),
        ]
        return [error for error in errores if error]