# core/views.py - ¡VERSIÓN FINAL Y CORREGIDA!

from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import Group 
from django.contrib.auth import get_user_model
from django.db import transaction

# Importaciones correctas y consolidadas
from productos.models import Producto, Categoria 
from .models import Pedido, ItemPedido 
from .forms import PedidoAnonimoForm
from .forms import CustomUserCreationForm, CustomUserChangeForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.http import JsonResponse

# Importar los formularios de Producto y Categoría
from productos.forms import ProductoForm, CategoriaForm


# --- FUNCIÓNES DE AYUDA ---

User = get_user_model()

def is_admin_user(user):
    """
    Verifica si el usuario es superusuario, staff, o pertenece al grupo 'Administradores'.
    """
    if user.is_authenticated:
        return user.is_staff or user.is_superuser or user.groups.filter(name='Administradores').exists()
    return False

def admin_required(function=None, redirect_field_name='next', login_url='core:login'):
    """
    Decorator for views that checks that the user is logged in and is an admin.
    """
    actual_decorator = user_passes_test(
        is_admin_user,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# --- VISTAS PÚBLICAS (ya existentes) ---

def home(request):
    productos_destacados = Producto.objects.filter(disponible=True).order_by('-creado')[:8] 
    categorias = Categoria.objects.all().order_by('nombre')

    context = {
        'productos_destacados': productos_destacados,
        'categorias': categorias,
        'titulo_pagina': 'Inicio - Zapatos y Mochilas Tejidos a Mano',
    }
    return render(request, 'core/home.html', context)


def about(request):
    context = {
        'titulo_pagina': 'Sobre Nosotros - Zapatos y Mochilas Tejidos a Mano',
    }
    return render(request, 'core/about.html', context)


def contact(request):
    context = {
        'titulo_pagina': 'Contacto - Zapatos y Mochilas Tejidos a Mano',
    }
    return render(request, 'core/contact.html', context)


@login_required
def profile(request):
    context = {
        'titulo_pagina': 'Perfil de Usuario',
    }
    return render(request, 'core/profile.html', context)


def register_view(request):
    if request.user.is_authenticated:
        if is_admin_user(request.user):
            return redirect('core:dashboard_home') 
        else:
            return redirect('core:home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Cuenta creada exitosamente para {user.username}!")

            try:
                email_subject = "¡Bienvenido a Tejidos a Mano!"
                html_message = render_to_string('core/email/registro_confirmacion.html', {
                    'username': user.username,
                    'email': user.email,
                })
                plain_message = strip_tags(html_message)

                email = EmailMessage(
                    email_subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                )
                email.content_subtype = "html"
                email.send()
                messages.info(request, "Se ha enviado un correo de bienvenida a tu dirección de email.")
            except Exception as e:
                messages.warning(request, f"Tu cuenta ha sido creada, pero no pudimos enviar el correo de bienvenida. Error: {e}")

            return redirect('core:home')
        else:
            messages.error(request, "Error al registrarse. Por favor, corrige los errores.")
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
        'titulo_pagina': 'Registro de Usuario',
    }
    return render(request, 'core/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        if is_admin_user(request.user):
            return redirect('core:dashboard_home') 
        else:
            return redirect('core:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido de nuevo, {username}!")

                if is_admin_user(user):
                    return redirect('core:dashboard_home') 
                else:
                    next_page = request.GET.get('next')
                    return redirect(next_page or 'core:home')
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Error en el formulario de login. Por favor, verifica tus credenciales.")
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
        'titulo_pagina': 'Iniciar Sesión',
    }
    return render(request, 'core/login.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('core:login')


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu perfil ha sido actualizado exitosamente!")
            return redirect('core:profile')
        else:
            messages.error(request, "Hubo un error al actualizar tu perfil. Por favor, revisa los datos.")
    else:
        form = CustomUserChangeForm(instance=request.user)

    context = {
        'form': form,
        'titulo_pagina': 'Editar Perfil',
    }
    return render(request, 'core/profile_edit.html', context)


def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Tu carrito está vacío. ¡Añade algunos productos!")
        return redirect('core:home')

    productos_en_carrito = []
    total_carrito = Decimal('0.00')
    for product_id, item_data in cart.items():
        try:
            product = Producto.objects.get(id=product_id)
            cantidad = item_data.get('cantidad', 1)
            precio_unitario = product.precio
            subtotal = precio_unitario * cantidad
            productos_en_carrito.append({
                'product': product,
                'cantidad': cantidad,
                'precio_unitario': precio_unitario,
                'subtotal': subtotal
            })
            total_carrito += subtotal
        except Producto.DoesNotExist:
            messages.error(request, f"Un producto en tu carrito (ID: {product_id}) no está disponible.")
            del cart[product_id]
            request.session['cart'] = cart
            return redirect('core:checkout')

    if request.method == 'POST':
        form = PedidoAnonimoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)

            if request.user.is_authenticated:
                pedido.usuario = request.user
            else:
                pedido.usuario = None

            pedido.total_pedido = total_carrito
            pedido.save()

            for item in productos_en_carrito:
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=item['product'],
                    precio=item['precio_unitario'],
                    cantidad=item['cantidad']
                )

            del request.session['cart']
            request.session.modified = True

            try:
                html_message = render_to_string('core/email/pedido_confirmacion.html', {
                    'pedido': pedido,
                    'productos_en_carrito': productos_en_carrito,
                    'total_carrito': total_carrito,
                })
                plain_message = strip_tags(html_message)

                email_subject = f"Confirmación de tu Pedido #{pedido.id} en Mi Tienda"
                recipient_list = [pedido.email]

                email = EmailMessage(
                    email_subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                )
                email.content_subtype = "html"
                email.send()
                messages.success(request, f"Tu pedido ha sido realizado exitosamente. Se ha enviado una confirmación a {pedido.email}.")
            except Exception as e:
                messages.error(request, f"Tu pedido ha sido realizado, pero no pudimos enviar el correo de confirmación. Error: {e}")

            if not request.user.is_authenticated:
                request.session['last_order_id'] = pedido.id

            return redirect('core:pedido_confirmado', pedido_id=pedido.id)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'nombre_completo': f"{request.user.first_name} {request.user.last_name}".strip(),
                'email': request.user.email,
            }
        form = PedidoAnonimoForm(initial=initial_data)

    context = {
        'form': form,
        'productos_en_carrito': productos_en_carrito,
        'total_carrito': total_carrito,
        'title': 'Finalizar Compra'
    }
    return render(request, 'core/checkout.html', context)


def pedido_confirmado_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    allowed_access = False
    if request.user.is_authenticated:
        if request.user == pedido.usuario or is_admin_user(request.user):
            allowed_access = True
    elif 'last_order_id' in request.session and request.session['last_order_id'] == pedido.id:
        allowed_access = True

    if not allowed_access:
        messages.error(request, "Acceso denegado o pedido no encontrado.")
        return redirect('core:home')

    return render(request, 'core/pedido_confirmado.html', {'pedido': pedido, 'title': 'Pedido Confirmado'})


# --- VISTAS DEL DASHBOARD (NUEVAS Y AMPLIADAS) ---

@admin_required(login_url='core:login') 
def dashboard_home(request):
    """
    Vista de la página principal del Dashboard.
    Aquí se muestran estadísticas y un resumen.
    """
    total_productos = Producto.objects.count()
    productos_disponibles = Producto.objects.filter(disponible=True).count()
    total_categorias = Categoria.objects.count()
    total_pedidos = Pedido.objects.count()
    pedidos_pendientes = Pedido.objects.filter(estado='pendiente').count()
    total_usuarios = User.objects.count()

    context = {
        'total_productos': total_productos,
        'productos_disponibles': productos_disponibles,
        'pedidos_pendientes': pedidos_pendientes,
        'total_pedidos': total_pedidos,
        'total_categorias': total_categorias,
        'total_usuarios': total_usuarios,
        'titulo_pagina': 'Dashboard de Administración',
    }
    return render(request, 'core/dashboard_home.html', context)


@admin_required(login_url='core:login')
def producto_lista_admin(request):
    """
    Lista todos los productos en el dashboard.
    """
    productos = Producto.objects.all().order_by('nombre')
    context = {
        'productos': productos,
        'titulo_pagina': 'Administrar Productos',
    }
    return render(request, 'core/dashboard_productos_lista.html', context)


@admin_required(login_url='core:login')
def producto_crear_admin(request):
    """
    Vista para crear un nuevo producto.
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, "¡Producto creado exitosamente!")
            return redirect('core:producto_lista_admin')
        else:
            messages.error(request, "Error al crear el producto. Por favor, revisa los datos.")
    else:
        form = ProductoForm()

    context = {
        'form': form,
        'titulo_pagina': 'Crear Nuevo Producto',
    }
    return render(request, 'core/dashboard_producto_form.html', context)


@admin_required(login_url='core:login')
def producto_editar_admin(request, pk):
    """
    Vista para editar un producto existente.
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f"¡Producto '{producto.nombre}' actualizado exitosamente!")
            return redirect('core:producto_lista_admin')
        else:
            messages.error(request, "Error al actualizar el producto. Por favor, revisa los datos.")
    else:
        form = ProductoForm(instance=producto)

    context = {
        'form': form,
        'titulo_pagina': f'Editar Producto: {producto.nombre}',
        'producto': producto, 
    }
    return render(request, 'core/dashboard_producto_form.html', context)


@admin_required(login_url='core:login')
def producto_eliminar_admin(request, pk):
    """
    Vista para eliminar un producto (con confirmación).
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, f"¡Producto '{producto.nombre}' eliminado exitosamente!")
        return redirect('core:producto_lista_admin')

    context = {
        'producto': producto, 
        'titulo_pagina': f'Confirmar Eliminación: {producto.nombre}',
    }
    return render(request, 'core/dashboard_producto_confirm_delete.html', context)


# --- NUEVAS VISTAS PARA EL DASHBOARD ---

@admin_required(login_url='core:login')
def categoria_lista_admin(request):
    """
    Lista todas las categorías en el dashboard.
    """
    categorias = Categoria.objects.all().order_by('nombre')
    context = {
        'categorias': categorias,
        'titulo_pagina': 'Administrar Categorías',
    }
    return render(request, 'core/dashboard_categorias_lista.html', context)

@admin_required(login_url='core:login')
def categoria_crear_admin(request):
    """
    Vista para crear una nueva categoría.
    """
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Categoría creada exitosamente!")
            return redirect('core:categoria_lista_admin')
        else:
            messages.error(request, "Error al crear la categoría. Por favor, revisa los datos.")
    else:
        form = CategoriaForm()
    
    context = {
        'form': form,
        'titulo_pagina': 'Crear Nueva Categoría',
    }
    return render(request, 'core/dashboard_categoria_form.html', context)

@admin_required(login_url='core:login')
def categoria_editar_admin(request, pk):
    """
    Vista para editar una categoría existente.
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, f"¡Categoría '{categoria.nombre}' actualizada exitosamente!")
            return redirect('core:categoria_lista_admin')
        else:
            messages.error(request, "Error al actualizar la categoría. Por favor, revisa los datos.")
    else:
        form = CategoriaForm(instance=categoria)

    context = {
        'form': form,
        'titulo_pagina': f'Editar Categoría: {categoria.nombre}',
        'categoria': categoria,
    }
    return render(request, 'core/dashboard_categoria_form.html', context)

@admin_required(login_url='core:login')
def categoria_eliminar_admin(request, pk):
    """
    Vista para eliminar una categoría (con confirmación).
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, f"¡Categoría '{categoria.nombre}' eliminada exitosamente!")
        return redirect('core:categoria_lista_admin')

    context = {
        'categoria': categoria,
        'titulo_pagina': f'Confirmar Eliminación: {categoria.nombre}',
    }
    return render(request, 'core/dashboard_categoria_confirm_delete.html', context)

@admin_required(login_url='core:login')
def pedido_lista_admin(request):
    """
    Lista todos los pedidos en el dashboard.
    """
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    context = {
        'pedidos': pedidos,
        'titulo_pagina': 'Administrar Pedidos',
    }
    return render(request, 'core/dashboard_pedidos_lista.html', context)

@admin_required(login_url='core:login')
def usuario_lista_admin(request):
    """
    Lista todos los usuarios en el dashboard.
    """
    usuarios = User.objects.all().order_by('username')
    context = {
        'usuarios': usuarios,
        'titulo_pagina': 'Administrar Usuarios',
    }
    return render(request, 'core/dashboard_usuarios_lista.html', context)

@admin_required(login_url='core:login')
def usuario_editar_admin(request, pk):
    """
    Vista para editar el estado 'is_active' de un usuario, solo para staff.
    """
    user_to_edit = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user_to_edit.is_active = not user_to_edit.is_active
        user_to_edit.save()
        messages.success(request, f'El estado de {user_to_edit.username} ha sido actualizado.')
        return redirect('core:usuario_lista_admin')
    
    context = {
        'user_to_edit': user_to_edit,
        'titulo_pagina': 'Editar Usuario',
    }
    return render(request, 'core/dashboard_usuario_editar.html', context)

@admin_required(login_url='core:login')
def usuario_eliminar_admin(request, pk):
    """
    Vista para confirmar y borrar un usuario, solo para staff.
    """
    user_to_delete = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        if user_to_delete == request.user:
            messages.error(request, 'No puedes borrar tu propia cuenta.')
            return redirect('core:usuario_lista_admin')
            
        user_to_delete.delete()
        messages.success(request, f'El usuario "{user_to_delete.username}" ha sido borrado exitosamente.')
        return redirect('core:usuario_lista_admin')
    
    context = {
        'user_to_delete': user_to_delete,
        'titulo_pagina': 'Confirmar Borrado',
    }
    return render(request, 'core/dashboard_usuario_eliminar.html', context)

# --- VISTAS PARA EL CARRITO ---

def cart_view(request):
    """
    Vista para mostrar el contenido del carrito.
    """
    cart = request.session.get('cart', {})
    productos_en_carrito = []
    total_carrito = Decimal('0.00')

    for product_id, item_data in cart.items():
        try:
            product = get_object_or_404(Producto, id=product_id)
            cantidad = item_data.get('cantidad', 1)
            precio_unitario = product.precio
            subtotal = precio_unitario * cantidad
            productos_en_carrito.append({
                'product': product,
                'cantidad': cantidad,
                'precio_unitario': precio_unitario,
                'subtotal': subtotal
            })
            total_carrito += subtotal
        except Producto.DoesNotExist:
            del cart[product_id]
            request.session.modified = True
            messages.warning(request, f"Un producto en tu carrito ya no está disponible y fue eliminado.")

    context = {
        'productos_en_carrito': productos_en_carrito,
        'total_carrito': total_carrito,
        'titulo_pagina': 'Tu Carrito de Compras',
    }
    return render(request, 'core/cart.html', context)


def add_to_cart(request, product_id):
    """
    Vista para agregar un producto al carrito o actualizar su cantidad.
    """
    if request.method == 'POST':
        try:
            product = get_object_or_404(Producto, id=product_id)
            cantidad = int(request.POST.get('cantidad', 1))
            
            cart = request.session.get('cart', {})
            product_id_str = str(product.id)
            
            if product_id_str in cart:
                cart[product_id_str]['cantidad'] += cantidad
                messages.success(request, f"Se han agregado {cantidad} unidades más de '{product.nombre}' a tu carrito.")
            else:
                cart[product_id_str] = {
                    'cantidad': cantidad,
                    'precio': str(product.precio)
                }
                messages.success(request, f"'{product.nombre}' ha sido agregado a tu carrito.")

            request.session['cart'] = cart
            request.session.modified = True
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Producto agregado al carrito con éxito', 'cart_count': len(cart)})
            
            # ¡CORRECCIÓN! Redirige a la vista del carrito con el nombre correcto.
            return redirect('core:cart_view')

        except Producto.DoesNotExist:
            messages.error(request, "El producto que intentas agregar no existe.")
        except ValueError:
            messages.error(request, "La cantidad debe ser un número entero válido.")

    return redirect('core:home')


def remove_from_cart(request, product_id):
    """
    Vista para eliminar un producto del carrito.
    """
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        product = get_object_or_404(Producto, id=product_id)
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f"'{product.nombre}' ha sido eliminado de tu carrito.")
    else:
        messages.error(request, "El producto no se encontró en tu carrito.")

    return redirect('core:cart_view')


def update_cart(request):
    """
    Vista para actualizar la cantidad de un producto en el carrito.
    """
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            new_cantidad = int(request.POST.get('cantidad', 1))
            if new_cantidad <= 0:
                messages.error(request, "La cantidad debe ser mayor que cero.")
                return redirect('core:cart_view')
        except (ValueError, TypeError):
            messages.error(request, "Cantidad inválida.")
            return redirect('core:cart_view')

        cart = request.session.get('cart', {})
        product_id_str = str(product_id)

        if product_id_str in cart:
            cart[product_id_str]['cantidad'] = new_cantidad
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, "Carrito actualizado.")
        else:
            messages.error(request, "El producto no se encontró en tu carrito.")

    return redirect('core:cart_view')
