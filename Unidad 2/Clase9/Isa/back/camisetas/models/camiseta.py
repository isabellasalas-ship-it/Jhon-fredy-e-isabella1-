from django.db import models


class Camiseta(models.Model):
    color = models.CharField(max_length=100)  # texto
    talla = models.CharField(max_length=2)   # texto
    material = models.CharField(max_length=100)            # texto
    fecha_creacion = models.DateField()                        # fecha
    marca= models.CharField(max_length=30)  # texto
    activa = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["color"]
    def __str__(self):
        return self.color