from rest_framework import serializers

from camisetas.models import Camiseta


class CamisetaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Camiseta
        fields = ["id", "color", "talla", "material", "fecha_creacion"]

    def validate_talla(self, value):
        if not 1 <= value <= 60:
            raise serializers.ValidationError(
                "La talla debe estar entre 1 y 60."
            )
        return value