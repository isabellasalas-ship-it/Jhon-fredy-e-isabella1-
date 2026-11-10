import requests

URL_BASE = "http://127.0.0.1:8000/api"
TIMEOUT = 5  # segundos que esperamos al servidor


class ErrorConexion(Exception):
    """El servidor no responde."""


class ErrorAPI(Exception):
    """El servidor respondió con un error (400, 404, 409...)."""

    def __init__(self, codigo, mensaje):
        super().__init__(mensaje)
        self.codigo = codigo
        self.mensaje = mensaje


class ClienteAPI:
    def _peticion(self, metodo, ruta, **kwargs):
        try:
            r = requests.request(
                metodo, f"{URL_BASE}{ruta}", timeout=TIMEOUT, **kwargs
            )
        except requests.exceptions.RequestException:
            raise ErrorConexion("No se pudo conectar con el servidor.")

        if r.status_code in (200, 201):
            return r.json()
        if r.status_code == 204:
            return None
        raise ErrorAPI(r.status_code, self._extraer_mensaje(r))

    def _extraer_mensaje(self, r):
        try:
            datos = r.json()
        except ValueError:
            return f"Error {r.status_code}"
        if isinstance(datos, dict):
            if "detail" in datos:
                return str(datos["detail"])
            partes = []
            for campo, errores in datos.items():
                if isinstance(errores, list):
                    errores = " ".join(str(e) for e in errores)
                if campo == "non_field_errors":
                    partes.append(str(errores))
                else:
                    partes.append(f"{campo}: {errores}")
            return "\n".join(partes)
        if isinstance(datos, list):
            return " ".join(str(e) for e in datos)
        return f"Error {r.status_code}"

    # ---------- Productos ----------
    def listar_productos(self):                      # GET
        return self._peticion("GET", "/productos/")

    def crear_producto(self, datos):                 # POST
        return self._peticion("POST", "/productos/", json=datos)

    def editar_producto(self, id_producto, datos):   # PUT
        return self._peticion("PUT", f"/productos/{id_producto}/", json=datos)

    def cambiar_activo(self, id_producto, activo):   # PATCH
        return self._peticion(
            "PATCH", f"/productos/{id_producto}/", json={"activo": activo}
        )

    def eliminar_producto(self, id_producto):        # DELETE
        return self._peticion("DELETE", f"/productos/{id_producto}/")

    # ---------- Ventas ----------
    def listar_ventas(self):
        return self._peticion("GET", "/ventas/")

    def crear_venta(self, datos):
        return self._peticion("POST", "/ventas/", json=datos)

    def eliminar_venta(self, id_venta):
        return self._peticion("DELETE", f"/ventas/{id_venta}/")

    # ---------- Detalles ----------
    def listar_detalles(self, id_venta):
        return self._peticion("GET", "/detalles/", params={"venta": id_venta})

    def crear_detalle(self, datos):
        return self._peticion("POST", "/detalles/", json=datos)

    def eliminar_detalle(self, id_detalle):
        return self._peticion("DELETE", f"/detalles/{id_detalle}/")