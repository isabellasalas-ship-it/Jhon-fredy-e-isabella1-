from rest_framework import viewsets

from camisetas.models import Camiseta
from camisetas.serializers import CamisetaSerializer


class CamisetaViewSet(viewsets.ModelViewSet):
    queryset = Camiseta.objects.all()
    serializer_class = CamisetaSerializer