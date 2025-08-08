# productos/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Producto, Categoria 
from decimal import Decimal

# Vistas principales para la gestión de productos y categorías.
# Cada vista debe tener un comentario explicativo sobre su propósito y uso.
# Si se agregan nuevas vistas, documentar su funcionalidad y parámetros importantes.

def lista_productos(request, categoria_slug=None):
    """
    Muestra la lista de productos disponibles, con la opción de filtrar por categoría.
    """
    categoria_seleccionada = None
    if categoria_slug:
        categoria_seleccionada = get_object_or_404(Categoria, slug=categoria_slug)
        productos = Producto.objects.filter(disponible=True, categoria=categoria_seleccionada)
        titulo = f"Productos - {categoria_seleccionada.nombre}"
    else:
        productos = Producto.objects.filter(disponible=True)
        titulo = "Todos los Productos"

    categorias = Categoria.objects.all() 

    # ¡CORRECCIÓN! El nombre de la plantilla debe ser 'productos/lista_productos.html'
    return render(request, 'productos/lista_productos.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
        'titulo_pagina': titulo
    })


def detalle_producto(request, id, slug):
    """
    Muestra los detalles de un producto específico.
    """
    producto = get_object_or_404(Producto, id=id, slug=slug, disponible=True)
    return render(request, 'productos/detalle_producto.html', {'producto': producto, 'titulo_pagina': producto.nombre})


def add_to_cart_simple(request, product_id):
    """
    Vista simple para agregar un producto al carrito directamente desde la lista de productos.
    """
    product = get_object_or_404(Producto, id=product_id)
    cantidad = 1

    cart = request.session.get('cart', {})
    product_id_str = str(product.id)

    if product_id_str in cart:
        cart[product_id_str]['cantidad'] += cantidad
    else:
        cart[product_id_str] = {'cantidad': cantidad, 'precio': str(product.precio)}

    request.session['cart'] = cart
    request.session.modified = True

    messages.success(request, f"'{product.nombre}' ha sido agregado a tu carrito.")
    # Redirige a la misma página para que el usuario siga comprando
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))

