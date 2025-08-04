# core/urls.py - ¡VERSIÓN AMPLIADA PARA EL DASHBOARD!

from django.urls import path
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
    path('checkout/', views.checkout_view, name='checkout'),
    path('pedido-confirmado/<int:pedido_id>/', views.pedido_confirmado_view, name='pedido_confirmado'),

    # --- URLS DEL DASHBOARD (NUEVAS) ---
    # Rutas para el Panel de Administración
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/productos/', views.producto_lista_admin, name='producto_lista_admin'),
    path('dashboard/productos/crear/', views.producto_crear_admin, name='producto_crear_admin'),
    path('dashboard/productos/editar/<int:pk>/', views.producto_editar_admin, name='producto_editar_admin'),
    path('dashboard/productos/eliminar/<int:pk>/', views.producto_eliminar_admin, name='producto_eliminar_admin'),

    # Nuevas URLs para el dashboard
    path('dashboard/categorias/', views.categoria_lista_admin, name='categoria_lista_admin'),
    path('dashboard/pedidos/', views.pedido_lista_admin, name='pedido_lista_admin'),
    path('dashboard/usuarios/', views.usuario_lista_admin, name='usuario_lista_admin'),
    path('dashboard/usuarios/', views.usuario_lista_admin, name='usuario_lista_admin'),
    path('dashboard/usuarios/editar/<int:pk>/', views.usuario_editar_admin, name='usuario_editar_admin'),
    path('dashboard/usuarios/eliminar/<int:pk>/', views.usuario_eliminar_admin, name='usuario_eliminar_admin'),
]
