# tejidos_web/urls.py

from django.contrib import admin
from django.urls import path, include # Importa 'include' para poder incluir las URLs de otras apps
from django.conf import settings # Importa 'settings' para acceder a la configuración del proyecto
from django.conf.urls.static import static # Importa 'static' para servir archivos estáticos/media en desarrollo

urlpatterns = [
    path('admin/', admin.site.urls), # Mapea la URL '/admin/' al panel de administración de Django.
    path('', include('core.urls')),
    path('productos/', include('productos.urls')), 
   path('servicios/', include(('servicios.urls', 'servicios'), namespace='servicios')),
  
   

]

# Configuración para servir archivos de medios durante el desarrollo
if settings.DEBUG:
    # `if settings.DEBUG`: Esta condición asegura que el servidor de desarrollo de Django
    # solo sirva archivos de medios cuando `DEBUG` es True (es decir, en desarrollo).
    # ¡Nunca uses esto en producción! En producción, un servidor web como Nginx o Apache
    # es el encargado de servir los archivos estáticos y de medios.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # `urlpatterns +=`: Añade nuevas reglas de URL a la lista existente.
    # `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`: Esta función
    # de Django crea patrones de URL que permiten al servidor de desarrollo servir
    # archivos desde la ruta especificada por `MEDIA_ROOT` cuando se accede a través de `MEDIA_URL`.
