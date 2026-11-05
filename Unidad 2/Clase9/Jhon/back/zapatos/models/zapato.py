from django.db import models


class Zapato(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100, unique=True)
    talla = models.PositiveSmallIntegerField()            
    fecha_creacion = models.DateField()                        # fecha

    class Meta:
        ordering = ["modelo"]

    def __str__(self):
        return self.modelo


"""class Clase(models.Model):
    zapato = models.ForeignKey(
        Zapato,
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
        return f"{self.asignatura} · {self.tema}" """