from django.db import models


class Asignatura(models.Model):
    nombre = models.CharField(max_length=100, unique=True)   # texto
    creditos = models.PositiveSmallIntegerField()            # entero
    activa = models.BooleanField(default=True)               # booleano
    fecha_inicio = models.DateField()                        # fecha

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Clase(models.Model):
    asignatura = models.ForeignKey(
        Asignatura,
        on_delete=models.CASCADE,
        related_name="clases",
    )
    tema = models.CharField(max_length=150)                  # texto
    fecha = models.DateField()                               # fecha
    hora_inicio = models.TimeField()                         # hora
    duracion_horas = models.DecimalField(                    # decimal
        max_digits=3, decimal_places=1
    )

    class Meta:
        ordering = ["fecha", "hora_inicio"]

    def __str__(self):
        return f"{self.asignatura} · {self.tema}"