import requests


class ErrorComunicacion(Exception):

    def __init__(self, mensaje, codigo=None):
        super().__init__(mensaje)
        self.codigo = codigo


class Comunicacion():

    def __init__(self):
        self.url = 'http://127.0.0.1:8000/api/'

    def peticion(self, metodo, ruta, datos=None, filtros=None):
        try:
            respuesta = requests.request(
                metodo, self.url + ruta, json=datos, params=filtros, timeout=5
            )
        except requests.RequestException:
            raise ErrorComunicacion(
                'No se pudo conectar con el servidor. ¿Está encendido el backend?'
            )

        if respuesta.status_code in (200, 201):
            return respuesta.json()
        if respuesta.status_code == 204:
            return None
        raise ErrorComunicacion(self.mensaje_error(respuesta), respuesta.status_code)

    def mensaje_error(self, respuesta):
        if respuesta.status_code == 404:
            return 'El registro ya no existe en el servidor.'
        try:
            errores = respuesta.json()
        except ValueError:
            return 'El servidor respondió con el error ' + str(respuesta.status_code) + '.'
        if not isinstance(errores, dict):
            return str(errores)

        mensajes = []
        for campo, detalle in errores.items():
            texto = ' '.join(detalle) if isinstance(detalle, list) else str(detalle)
            if campo in ('detail', 'non_field_errors'):
                mensajes.append(texto)
            else:
                mensajes.append(campo + ': ' + texto)
        return '\n'.join(mensajes)

    def listar(self, recurso, filtros=None):                 
        return self.peticion('GET', recurso + '/', filtros=filtros)

    def consultar(self, recurso, id):                        
        return self.peticion('GET', recurso + '/' + str(id) + '/')

    def crear(self, recurso, datos):                         
        return self.peticion('POST', recurso + '/', datos)

    def reemplazar(self, recurso, id, datos):                
        return self.peticion('PUT', recurso + '/' + str(id) + '/', datos)

    def modificar(self, recurso, id, datos):                
        return self.peticion('PATCH', recurso + '/' + str(id) + '/', datos)

    def eliminar(self, recurso, id):                         
        return self.peticion('DELETE', recurso + '/' + str(id) + '/')