# productos/urls.py

from django.urls import path # Importa 'path' para definir patrones de URL.
from . import views # Importa las vistas de la aplicación actual (productos/views.py).

app_name = 'productos' # Define un nombre de espacio para estas URLs. Evita conflictos con URLs de otras apps.

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    # `path('')`: Mapea la URL raíz de esta aplicación (ej: /productos/) a la vista `lista_productos`.
    # `name='lista_productos'`: Nombre para referenciar esta URL en plantillas o código (ej: {% url 'productos:lista_productos' %}).

    path('<slug:categoria_slug>/', views.lista_productos, name='lista_productos_por_categoria'),
    # `path('<slug:categoria_slug>/')`: Captura un "slug" (texto amigable para URL) de la URL.
    # `slug:categoria_slug`: Dice que la parte de la URL capturada es un slug y se llamará `categoria_slug`.
    # Esta misma vista (`lista_productos`) se usa para listar productos, pero con un filtro de categoría.

    path('<int:id>/<slug:slug>/', views.detalle_producto, name='detalle_producto'),
    # `path('<int:id>/<slug:slug>/')`: Captura un número entero (`id`) y un slug (`slug`).
    # Es común usar ambos para el detalle de un producto para SEO y unicidad.
    # `id`: Corresponderá al `id` del producto.
    # `slug`: Corresponderá al `slug` del producto.
]