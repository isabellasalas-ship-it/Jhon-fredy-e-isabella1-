from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class Venta(models.Model):
    METODOS_PAGO = [
        ("EFECTIVO", "Efectivo"),
        ("TARJETA", "Tarjeta"),
        ("TRANSFERENCIA", "Transferencia"),
    ]

    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=100)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Venta {self.id} - {self.cliente}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
