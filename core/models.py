# core/models.py - ¡ASEGÚRATE DE QUE ESTÉ ASÍ!

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# ¡IMPORTANTE! Importa Categoria y Producto desde la app 'productos'
from productos.models import Categoria, Producto # <--- DEBE ESTAR ESTA IMPORTACIÓN Y NINGUNA DEFINICIÓN ABAJO

# 3. Definir Pedido, ya que ItemPedido depende de ella
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos')
    nombre_completo = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion_envio = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    pais = models.CharField(max_length=100, default='Colombia')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ESTADO_PEDIDO = (
        ('pendiente', 'Pendiente'), ('procesando', 'Procesando'), ('enviado', 'Enviado'),
        ('completado', 'Completado'), ('cancelado', 'Cancelado'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_PEDIDO, default='pendiente')
    hecho_por_admin = models.BooleanField(default=False)
    admin_observaciones = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-fecha_pedido']
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido {self.id} de {self.nombre_completo}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

# 4. Definir ItemPedido al final, ya que depende de Pedido y Producto
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = "Items de Pedido"

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre if self.producto else 'Producto Eliminado'}"

    def get_cost(self):
        return self.precio * self.cantidad
