from decimal import Decimal

from rest_framework import serializers

from .models import Asignatura, Clase


class ClaseSerializer(serializers.ModelSerializer):
    # Campo extra, solo lectura, tomado de la relación
    asignatura_nombre = serializers.CharField(
        source="asignatura.nombre", read_only=True
    )

    class Meta:
        model = Clase
        fields = [
            "id", "asignatura", "asignatura_nombre",
            "tema", "fecha", "hora_inicio", "duracion_horas",
        ]

    # Validación de un campo: validate_<nombre_del_campo>
    def validate_duracion_horas(self, value):
        if not Decimal("0.5") <= value <= Decimal("4"):
            raise serializers.ValidationError(
                "La duración debe estar entre 0.5 y 4 horas."
            )
        return value

    # Validación que involucra varios campos
    def validate(self, data):
        # En un PATCH, lo que no se envía se toma del objeto existente
        asignatura = data.get("asignatura", getattr(self.instance, "asignatura", None))
        fecha = data.get("fecha", getattr(self.instance, "fecha", None))

        if asignatura and not asignatura.activa:
            raise serializers.ValidationError(
                "No se pueden programar clases en una asignatura inactiva."
            )
        if asignatura and fecha and fecha < asignatura.fecha_inicio:
            raise serializers.ValidationError(
                {"fecha": "La clase no puede ser anterior al inicio de la asignatura."}
            )
        return data


class AsignaturaSerializer(serializers.ModelSerializer):
    # Serializer anidado: muestra las clases dentro de la asignatura
    clases = ClaseSerializer(many=True, read_only=True)
    # Campo calculado
    total_clases = serializers.SerializerMethodField()

    class Meta:
        model = Asignatura
        fields = [
            "id", "nombre", "creditos", "activa",
            "fecha_inicio", "total_clases", "clases",
        ]

    def get_total_clases(self, obj):
        return obj.clases.count()

    def validate_creditos(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                "Los créditos deben estar entre 1 y 10."
            )
        return value