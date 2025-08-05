# core/context_processors.py

def cart_item_count(request):
    """
    Un procesador de contexto que añade el número total de ítems en el carrito
    a todas las plantillas.
    """
    cart = request.session.get('cart', {})
    total_items = sum(item_data.get('cantidad', 0) for item_data in cart.values())
    return {'cart_item_count': total_items}

