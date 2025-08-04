# servicios/admin.py

from django.contrib import admin
from .models import Servicio, SolicitudServicio # Importa los modelos de la app servicios.

# Registrar el modelo Servicio
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_referencia', 'disponible', 'creado', 'actualizado')
    list_filter = ('disponible', 'creado', 'actualizado')
    list_editable = ('precio_referencia', 'disponible')
    prepopulated_fields = {'slug': ('nombre',)}

# Registrar el modelo SolicitudServicio
@admin.register(SolicitudServicio)
class SolicitudServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre_cliente', 'email_cliente', 'servicio', 'fecha_solicitud', 'resuelto')
    list_filter = ('resuelto', 'fecha_solicitud', 'servicio')
    list_editable = ('resuelto',)
    search_fields = ('nombre_cliente', 'email_cliente', 'mensaje')
    # `search_fields`: Añade una barra de búsqueda en la parte superior del admin para buscar en estos campos.

# Register your models here.
