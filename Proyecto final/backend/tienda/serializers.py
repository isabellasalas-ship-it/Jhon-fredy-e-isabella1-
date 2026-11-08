from django.db import transaction
from rest_framework import serializers

from .models import Producto, Venta, DetalleVenta


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["id", "nombre", "precio", "stock", "activo"]


class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ["id", "venta", "producto", "cantidad", "precio_unitario"]
        read_only_fields = ["precio_unitario"]

    def validate(self, datos):
        # Solo se valida el stock al crear un detalle
        if self.instance is None:
            producto = datos["producto"]
            cantidad = datos["cantidad"]
            if not producto.activo:
                raise serializers.ValidationError(
                    "Ese producto ya no está a la venta."
                )
            if cantidad > producto.stock:
                raise serializers.ValidationError(
                    f"Solo hay {producto.stock} unidades de {producto.nombre}."
                )
        return datos

    @transaction.atomic
    def create(self, datos):
        producto = datos["producto"]
        datos["precio_unitario"] = producto.precio   # se copia el precio actual
        producto.stock -= datos["cantidad"]          # se descuenta el stock
        producto.save()
        return super().create(datos)


class VentaSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = ["id", "fecha", "cliente", "metodo_pago", "observaciones", "total"]
        read_only_fields = ["fecha"]

    def get_total(self, venta):
        return sum(
            d.cantidad * d.precio_unitario
            for d in venta.detalleventa_set.all()
        )