# servicios/urls.py
from django.urls import path
from . import views

app_name = 'servicios'

urlpatterns = [
    # Rutas públicas para los servicios/cursos
    path('', views.lista_servicios, name='lista_servicios'),
    path('<slug:slug>/', views.detalle_servicio, name='detalle_servicio'),

    # NOTA: Las rutas de administración de cursos se han movido a core/urls.py
    # ya que toda la lógica de administración se maneja en la aplicación 'core'.
]
