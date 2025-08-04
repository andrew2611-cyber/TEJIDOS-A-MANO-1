# productos/views.py

from django.shortcuts import render, get_object_or_404 # Importa 'render' y 'get_object_or_404'.
# `get_object_or_404`: Función útil para recuperar un objeto de la base de datos o lanzar un error 404 (página no encontrada) si el objeto no existe.
from .models import Producto, Categoria # Importa los modelos que definiste en productos/models.py.

def lista_productos(request, categoria_slug=None):
    """
    Vista para listar productos.
    Puede filtrar por categoría si se proporciona un slug de categoría.
    """
    categoria = None
    categorias = Categoria.objects.all() # Obtiene todas las categorías para mostrarlas en la navegación.
    productos = Producto.objects.filter(disponible=True) # Empieza con todos los productos disponibles.

    if categoria_slug:
        # Si se proporciona un slug de categoría en la URL
        categoria = get_object_or_404(Categoria, slug=categoria_slug)
        # Intenta obtener la categoría por su slug; si no la encuentra, lanza 404.
        productos = productos.filter(categoria=categoria)
        # Filtra los productos para mostrar solo los de la categoría seleccionada.

    context = {
        'categoria': categoria,
        'categorias': categorias,
        'productos': productos,
        'titulo_pagina': 'Nuestros Productos',
    }
    return render(request, 'productos/lista_productos.html', context)

def detalle_producto(request, id, slug):
    """
    Vista para mostrar los detalles de un producto específico.
    Se usan tanto el ID como el slug en la URL para mayor SEO y robustez.
    """
    producto = get_object_or_404(Producto,
                                 id=id,
                                 slug=slug,
                                 disponible=True)
    # Recupera el producto usando su ID y slug, y asegura que esté disponible.
    # Si no lo encuentra, lanza un error 404.

    context = {
        'producto': producto,
        'titulo_pagina': producto.nombre, # El título de la página será el nombre del producto.
    }
    return render(request, 'productos/detalle_producto.html', context)