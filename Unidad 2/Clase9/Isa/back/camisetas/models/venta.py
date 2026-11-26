from django.db import models


class Venta(models.Model):
    METODOS_PAGO = [
        ("EFECTIVO", "Efectivo"),
        ("TRANSFERENCIA", "Transferencia"),
    ]

    camiseta = models.ForeignKey(
        "camisetas.Camiseta", on_delete=models.PROTECT, related_name="ventas"
    )
    cliente = models.CharField(max_length=100)
    fecha = models.DateField()
    cantidad = models.PositiveSmallIntegerField()
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default="EFECTIVO")

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return self.cliente