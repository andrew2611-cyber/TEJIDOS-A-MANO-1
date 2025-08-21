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
        ('fondo.png', 'Fondo 1'),
        ('fondo1.png', 'Fondo 2'),
        ('fondo3.png', 'Fondo 3'),
        ('fondo4.png', 'Fondo 4'),
        ('mujer.png', 'Mujer'),
        ('mujer1.png', 'Mujer 2'),
        ('hombre.png', 'Hombre'),
        ('hombre1.png', 'Hombre 2'),
        ('servicios.png', 'Servicios'),
        ('imagen1defondo.png', 'tarjetas'),
    ]
    imagen_fondo = models.CharField(
        max_length=64,
        choices=FONDO_CHOICES,
        default='fondo.png',
        help_text="Imagen de fondo de la tarjeta (elige una de las imágenes del proyecto)"
    )
    imagen_3d = models.ImageField(upload_to='productos_3d/', blank=True, null=True, help_text="Imagen 3D del producto para la categoría")
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
