import requests

class ErrorComunicacion(Exception):
    """Error con un mensaje listo para mostrarle al usuario."""

class Comunicacion():

    def _init_(self):
        self.url = 'http://localhost:8000/'

    def peticion(self, metodo, ruta, datos=None):
        try:
            resultado = requests.request(metodo, self.url + ruta, json=datos, timeout=5)
        except requests.RequestException:
            raise ErrorComunicacion(
                'No se pudo conectar con el servidor. ¿Está corriendo el back?'
            )
        if not resultado.ok:
            raise ErrorComunicacion(self.mensaje_error(resultado))
        return resultado.json() if resultado.content else None

    def mensaje_error(self, resultado):
        try:
            errores = resultado.json()
        except ValueError:
            return 'El servidor respondió con error ' + str(resultado.status_code) + '.'

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

    def eliminar(self, recurso, id):
        return self.peticion('DELETE', '/' + recurso + '/' + str(id) + '/')

    def consultarAsignaturas(self):
        return self.peticion('GET', '/asignatura')

    def guardarAsignatura(self, datos, id=None):
        return self.guardar('asignatura', datos, id)

    def eliminarAsignatura(self, id):
        return self.eliminar('asignatura', id)

    def consultarClases(self):
        return self.peticion('GET', '/clase')

    def guardarClase(self, datos, id=None):
        return self.guardar('clase', datos, id)

    def eliminarClase(self, id):
        return self.eliminar('clase', id)