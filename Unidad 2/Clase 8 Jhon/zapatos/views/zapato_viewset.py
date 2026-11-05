from rest_framework import viewsets

from zapatos.models import Zapato
from zapatos.serializers import ZapatoSerializer


class ZapatoViewSet(viewsets.ModelViewSet):
    queryset = Zapato.objects.all()
    serializer_class = ZapatoSerializer