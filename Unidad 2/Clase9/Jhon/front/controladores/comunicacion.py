import requests

class ErrorComunicacion(Exception):
    """Error con un mensaje listo para mostrar al usuario."""

class Comunicacion():

    def __init__(self):
        self.url = 'http://localhost:8000/'

    def peticion(self, metodo, ruta, datos=None):
        try:
            resultado = requests.request(metodo, self.url + ruta, json=datos, timeout=5)

        except requests.RequestException:
            raise ErrorComunicacion(
                'No se pudo conectar con el servidor. ¿Esta corriendo el Back?'
            )

        if not resultado.ok:
            raise ErrorComunicacion(self.mensaje_error(resultado))
        return resultado.json() if resultado.content else None

    def mensaje_error(self, resultado):
        try:
            errores = resultado.json()
        except ValueError:
            return 'El servidor respondio con error ' + str(resultado.status_code) + '.'

        mensajes = []
        for campo, detalle in errores.items():
            texto = ' '.join(detalle) if isinstance(detalle, list) else str(detalle)
            if campo in ('detail', 'non_field_errors'):
                mensajes.append(texto)
            else:
                mensajes.append(campo + ': ' + texto)

        return '\n'.join(mensajes)

    def guardar(self, recurso, datos, id=None):
        if id is None:
            return self.peticion('POST', '/' + recurso, datos)
        return self.peticion('PUT', '/' + recurso + '/' + str(id) + '/', datos)