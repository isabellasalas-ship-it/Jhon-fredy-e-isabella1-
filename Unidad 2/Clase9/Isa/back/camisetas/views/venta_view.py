from rest_framework import viewsets

from camisetas.models import Venta
from camisetas.serializers import VentaSerializer


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer