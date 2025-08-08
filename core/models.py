from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# ¡IMPORTANTE! Importa Categoria y Producto desde la app 'productos'
from productos.models import Categoria, Producto # <--- DEBE ESTAR ESTA IMPORTACIÓN Y NINGUNA DEFINICIÓN ABAJO

# Modelos principales para la gestión de pedidos y sus ítems.
# Relacionan usuarios, productos y detalles del pedido.
# Se recomienda mantener estos comentarios para facilitar el trabajo colaborativo.
# Si se agregan nuevos campos, documentar su propósito y uso.

# 3. Definir Pedido, ya que ItemPedido depende de ella
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos') # Usuario que realiza el pedido
    nombre_completo = models.CharField(max_length=200) # Nombre del cliente
    email = models.EmailField() # Email de contacto
    telefono = models.CharField(max_length=20, blank=True, null=True) # Teléfono opcional
    direccion_envio = models.CharField(max_length=255) # Dirección de envío
    ciudad = models.CharField(max_length=100) # Ciudad de envío
    codigo_postal = models.CharField(max_length=10, blank=True, null=True) # Código postal opcional
    pais = models.CharField(max_length=100, default='Colombia') # País de envío
    fecha_pedido = models.DateTimeField(auto_now_add=True) # Fecha de creación
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Total calculado
    ESTADO_PEDIDO = (
        ('pendiente', 'Pendiente'), ('procesando', 'Procesando'), ('enviado', 'Enviado'),
        ('completado', 'Completado'), ('cancelado', 'Cancelado'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_PEDIDO, default='pendiente') # Estado del pedido
    hecho_por_admin = models.BooleanField(default=False) # Si el pedido fue gestionado por un admin
    admin_observaciones = models.TextField(blank=True, null=True) # Observaciones internas

    class Meta:
        ordering = ['-fecha_pedido']
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido {self.id} de {self.nombre_completo}"

    def get_total_cost(self):
        """
        Calcula el costo total sumando el costo de cada ítem del pedido.
        """
        return sum(item.get_cost() for item in self.items.all())

# 4. Definir ItemPedido al final, ya que depende de Pedido y Producto
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items') # Pedido asociado
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True) # Producto comprado
    precio = models.DecimalField(max_digits=10, decimal_places=2) # Precio unitario
    cantidad = models.PositiveIntegerField(default=1) # Cantidad solicitada

    class Meta:
        verbose_name_plural = "Items de Pedido"

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre if self.producto else 'Producto Eliminado'}"

    def get_cost(self):
        """
        Retorna el costo total de este ítem (precio * cantidad).
        """
        return self.precio * self.cantidad
