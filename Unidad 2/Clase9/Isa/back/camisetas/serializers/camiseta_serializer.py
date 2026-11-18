
from rest_framework import serializers

from camisetas.models import Camiseta


class CamisetaSerializer(serializers.ModelSerializer):

    def validate_talla(self, value):
        if value.upper() not in ["S", "M", "L", "XL"]:
            raise serializers.ValidationError(
                "La talla debe ser S, M, L o XL."
            )
        return value.upper()

    class Meta:
        model = Camiseta
        fields = ["id", "color", "talla", "material", "fecha_creacion", "marca"]
