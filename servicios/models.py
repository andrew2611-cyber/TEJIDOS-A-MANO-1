# servicios/models.py

from django.db import models

class Servicio(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text="URL amigable (ej: taller-tejido-basico)")
    descripcion_corta = models.TextField(blank=True, help_text="Breve resumen del servicio")
    descripcion_larga = models.TextField()
    precio_referencia = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Precio estimado o desde")
    # `blank=True, null=True`: Indica que este campo es opcional.
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)
    # `upload_to='servicios/'`: Directorio donde se guardarán las imágenes de los servicios.
    disponible = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Servicios"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class SolicitudServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True, blank=True, related_name='solicitudes')
    # `on_delete=models.SET_NULL`: Si el servicio al que se refiere la solicitud es eliminado, este campo se pondrá a NULL.
    # `null=True, blank=True`: Permite que la solicitud exista incluso si el servicio original ya no está.
    nombre_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField() # Campo específico para correos electrónicos.
    telefono_cliente = models.CharField(max_length=20, blank=True, null=True)
    mensaje = models.TextField(help_text="Detalles de la solicitud o pregunta")
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    resuelto = models.BooleanField(default=False)
    # `resuelto`: Campo para que el administrador marque si la solicitud ha sido procesada.

    class Meta:
        verbose_name_plural = "Solicitudes de Servicio"
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"Solicitud de {self.nombre_cliente} para {self.servicio.nombre if self.servicio else 'Servicio no especificado'}"
        # Muestra el nombre del servicio si existe, de lo contrario indica que no está especificado. Create your models here.
