from rest_framework import serializers

from camisetas.models import Venta


class VentaSerializer(serializers.ModelSerializer):
    camiseta_color = serializers.CharField(source="camiseta.color", read_only=True)

    class Meta:
        model = Venta
        fields = [
            "id", "camiseta", "camiseta_color", "cliente",
            "fecha", "cantidad", "metodo_pago",
        ]