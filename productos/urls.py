# productos/urls.py

from django.urls import path
from . import views

# Define un nombre de espacio para estas URLs. Evita conflictos con URLs de otras apps.
app_name = 'productos'

urlpatterns = [
    # Mapea la URL raíz de esta aplicación a la vista 'lista_productos'.
    path('', views.lista_productos, name='lista_productos'),

    # Captura un "slug" para filtrar productos por categoría.
    path('<slug:categoria_slug>/', views.lista_productos, name='lista_productos_por_categoria'),

    # Captura un ID y un slug para la página de detalle del producto.
    path('<int:id>/<slug:slug>/', views.detalle_producto, name='detalle_producto'),

    # ¡CORRECCIÓN! El nombre de la URL ahora coincide con lo que tu código busca.
    path('agregar-carrito-simple/<int:product_id>/', views.add_to_cart_simple, name='agregar-carrito-simple'),
]