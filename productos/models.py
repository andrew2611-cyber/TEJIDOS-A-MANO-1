# Modelos principales para la gestión de productos y categorías.
# Relacionan productos con categorías y gestionan atributos clave como stock y disponibilidad.
# Si se agregan nuevos campos, documentar su propósito y uso.

# productos/models.py

from django.db import models
from django.urls import reverse
from django.utils.text import slugify # Importa slugify

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, help_text="URL amigable (ej: zapatos-mujer)")
    descripcion = models.TextField(blank=True, null=True)

    # Nuevo campo para imagen de fondo de la tarjeta (solo elige entre imágenes existentes)
    FONDO_CHOICES = [
        
        ('imagen1defondo.png', 'tarjetas'),
        ('tarjeta1.png', 'tarjeta1'),
        ('tarjeta2.png', 'tarjeta2'),
        ('tarjeta3.png', 'tarjeta3'),

    ]
    imagen_fondo = models.CharField(
        max_length=64,
        choices=FONDO_CHOICES,
        default='fondo.png',
        help_text="Imagen de fondo de la tarjeta (elige una de las imágenes del proyecto)"
    )
    imagen_principal = models.ImageField(upload_to='productos_categoria/', blank=True, null=True, help_text="Imagen principal del producto para mostrar en la tarjeta de la categoría")

    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text="URL amigable (ej: zapato-flor)")
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_principal = models.ImageField(upload_to='productos/', blank=True, null=True, help_text="Imagen principal del producto")
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    FONDO_CHOICES = [
        ('fondo_zapatos_rosados.png', 'Zapatos Rosados'),
        ('tarjeta4.png', 'Tarjeta 4'),
        ('tarjeta5.png', 'Tarjeta 5'),
        ('tarjeta7.png', 'Tarjeta 7'),
        ('tarjeta8.png', 'Tarjeta 8'),

    ]
    imagen_fondo = models.CharField(
        max_length=64,
        choices=FONDO_CHOICES,
        default='fondo_zapatos_rosados.png',
        help_text="Imagen de fondo de la tarjeta del producto (elige una de las imágenes del proyecto)"
    )

    class Meta:
        ordering = ['-creado']
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        """
        Autogenera el slug único para el producto basado en el nombre.
        """
        if not self.slug: # Si el slug está vacío
            base_slug = slugify(self.nombre)
            unique_slug = base_slug
            num = 1
            # Asegura que el slug sea único
            while Producto.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('productos:detalle_producto', args=[self.id, self.slug])


class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos_galeria/')
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Imágenes de Productos"

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"
