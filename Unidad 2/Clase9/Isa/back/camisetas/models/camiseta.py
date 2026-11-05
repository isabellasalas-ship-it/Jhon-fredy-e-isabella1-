from django.db import models


class Camiseta(models.Model):
    color = models.CharField(max_length=100, unique=True)   # texto
    talla = models.PositiveSmallIntegerField()            # entero
    material = models.CharField(max_length=100)            # texto
    fecha_creacion = models.DateField()                        # fecha

    class Meta:
        ordering = ["color"]
    def __str__(self):
        return self.color