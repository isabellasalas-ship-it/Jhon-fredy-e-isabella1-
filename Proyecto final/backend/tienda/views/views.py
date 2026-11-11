from django.db import transaction
from django.db.models import ProtectedError
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Producto, Venta, DetalleVenta
from .serializers import (
    ProductoSerializer,
    VentaSerializer,
    DetalleVentaSerializer,
)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by("id")
    serializer_class = ProductoSerializer

    def destroy(self, request, *args, **kwargs):
        producto = self.get_object()
        try:
            producto.delete()
        except ProtectedError:
            return Response(
                {"detail": "No se puede eliminar: el producto ya fue vendido. "
                           "Desactívalo en su lugar."},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by("-fecha")
    serializer_class = VentaSerializer

    @transaction.atomic
    def perform_destroy(self, instance):
        # Al borrar la venta, las unidades vuelven a la bodega
        for detalle in instance.detalleventa_set.select_related("producto"):
            producto = detalle.producto
            producto.stock += detalle.cantidad
            producto.save()
        instance.delete()


class DetalleVentaViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleVentaSerializer

    def get_queryset(self):
        consulta = DetalleVenta.objects.all().order_by("id")
        venta_id = self.request.query_params.get("venta")
        if venta_id:
            consulta = consulta.filter(venta_id=venta_id)
        return consulta

    @transaction.atomic
    def perform_destroy(self, instance):
        # Al quitar un producto de la venta, vuelve a la bodega
        producto = instance.producto
        producto.stock += instance.cantidad
        producto.save()
        instance.delete()