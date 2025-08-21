# productos/admin.py

from django.contrib import admin # Necesario para interactuar con el admin de Django.
from .models import Categoria, Producto, ImagenProducto # Importa los modelos que acabamos de crear en la misma app.

# Registrar el modelo Categoria
@admin.register(Categoria) # Decorador de Django que simplifica el registro del modelo en el admin. Equivalente a `admin.site.register(Categoria, CategoriaAdmin)`.
class CategoriaAdmin(admin.ModelAdmin): # Define una clase de opciones para cómo se verá el modelo Categoria en el admin.
    list_display = ('nombre', 'slug', 'imagen_fondo')
    # `list_display`: Una tupla de nombres de campos que se mostrarán en la lista de objetos del admin.
    prepopulated_fields = {'slug': ('nombre',)}
    # `prepopulated_fields`: Un diccionario que autocompleta ciertos campos (aquí 'slug')
    # basándose en otros campos (aquí 'nombre') mientras el usuario escribe en el admin. Muy útil para slugs.
    list_editable = ('imagen_fondo',)

# Inline para añadir múltiples imágenes a un producto desde su formulario
class ImagenProductoInline(admin.TabularInline): # Define un "inline" para el modelo ImagenProducto. Los inlines permiten editar modelos relacionados en la misma página del modelo principal.
    model = ImagenProducto # Indica qué modelo se va a editar como inline.
    extra = 1 # Número de formularios extra vacíos que se mostrarán para añadir nuevas imágenes.

# Registrar el modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'disponible', 'creado', 'actualizado')
    list_filter = ('disponible', 'creado', 'actualizado', 'categoria')
    # `list_filter`: Permite añadir filtros en la barra lateral del admin para estos campos.
    list_editable = ('precio', 'disponible')
    # `list_editable`: Permite editar directamente estos campos desde la vista de lista de productos, sin tener que entrar a cada detalle.
    prepopulated_fields = {'slug': ('nombre',)}

    # `raw_id_fields`: En lugar de un desplegable, muestra un campo de texto con un botón de lupa
    # para buscar el ID de la categoría. Útil si hay muchísimas categorías.
    inlines = [ImagenProductoInline]
    # `inlines`: Asocia el inline `ImagenProductoInline` a la vista de edición del `Producto`.
    # Esto permite añadir/eliminar imágenes directamente al editar un producto.
