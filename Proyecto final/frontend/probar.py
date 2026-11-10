from cliente_api import ClienteAPI, ErrorConexion, ErrorAPI

cliente = ClienteAPI()

try:
    productos = cliente.listar_productos()
    print("Productos encontrados:", len(productos))
    for p in productos:
        print(p)
except ErrorConexion as e:
    print("Sin conexión:", e)
except ErrorAPI as e:
    print("Error de la API:", e.codigo, e.mensaje)