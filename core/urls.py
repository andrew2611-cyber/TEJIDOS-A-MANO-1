from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    # --- URLS PÚBLICAS Y DE USUARIO ---
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),

    # URLs PERSONALIZADAS PARA AUTENTICACIÓN
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),

    # URLs de Carrito y Pedido
    path('carrito/', views.cart_view, name='cart_view'),
    path('carrito/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('carrito/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('carrito/update/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('pedido-confirmado/<int:pedido_id>/', views.pedido_confirmado_view, name='pedido_confirmado'),

    # --- URLS DEL DASHBOARD (NUEVAS) ---
    # Rutas para el Panel de Administración
    path('dashboard/', views.dashboard_home, name='dashboard_home'),

    # Rutas para Productos
    path('dashboard/productos/', views.producto_lista_admin, name='producto_lista_admin'),
    path('dashboard/productos/crear/', views.producto_crear_admin, name='producto_crear_admin'),
    

    # Rutas para Categorías
    path('dashboard/categorias/', views.categoria_lista_admin, name='categoria_lista_admin'),
    path('dashboard/categorias/crear/', views.categoria_crear_admin, name='categoria_crear_admin'),
    path('dashboard/categorias/<int:pk>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),
   

    # Rutas para Pedidos (SIN pedido_cambiar_estado_admin)
    path('dashboard/pedidos/', views.pedido_lista_admin, name='pedido_lista_admin'),
    path('dashboard/pedidos/<int:pk>/detalle/', views.pedido_detalle_admin, name='pedido_detalle_admin'),


    # Rutas para Usuarios
    path('dashboard/usuarios/', views.usuario_lista_admin, name='usuario_lista_admin'),
    

    # --- RUTAS PARA CURSOS EN EL DASHBOARD ---
    path('dashboard/cursos/', views.curso_lista_admin, name='curso_lista_admin'),
    path('dashboard/cursos/crear/', views.curso_crear_admin, name='curso_crear_admin'),
    
    path('dashboard/cursos/<int:pk>/inscripciones/', views.inscripciones_curso_admin, name='inscripciones_curso_admin'),
    
    # Ruta para resultados de búsqueda
    path('buscar/', views.search_results, name='search_results'),

    # Ruta para página especial
    path('pagina-especial/', views.pagina_especial, name='pagina_especial'),

    # --- RECUPERACIÓN DE CONTRASEÑA ---
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='core/password_reset_form.html',
        email_template_name='core/password_reset_email.html',
        success_url='/password_reset/done/'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core/password_reset_complete.html'
    ), name='password_reset_complete'),
]
