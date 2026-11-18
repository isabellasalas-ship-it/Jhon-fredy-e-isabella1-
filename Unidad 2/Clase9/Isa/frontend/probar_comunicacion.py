from controladores.comunicacion import Comunicacion, ErrorComunicacion

comunicacion = Comunicacion()

datos = {
    'color': 'azul prueba',
    'talla': 'M',
    'material': 'algodon',
    'fecha_creacion': '2026-11-11',
    'marca': 'Marca de prueba',
}

try:
    creada = comunicacion.crear('camisetas', datos)
    id = creada['id']
    print('POST   creada con id', id)

    print('GET    hay', len(comunicacion.listar('camisetas')), 'camisetas')
    print('GET    consultada:', comunicacion.consultar('camisetas', id)['color'])

    datos['marca'] = 'Marca modificada'
    print('PUT    marca:', comunicacion.reemplazar('camisetas', id, datos)['marca'])

    cambio = {'material': 'algodon modificado'}
    print('PATCH  material:', comunicacion.modificar('camisetas', id, cambio)['material'])

    comunicacion.eliminar('camisetas', id)
    print('DELETE eliminada')
except ErrorComunicacion as error:
    print('Algo falló:', error)

try:
    comunicacion.consultar('camisetas', 999999)
except ErrorComunicacion as error:
    print('Código', error.codigo, '->', error)

try:
    datos['talla'] = 'XS'
    comunicacion.crear('camisetas', datos)
except ErrorComunicacion as error:
    print('Código', error.codigo, '->', error)