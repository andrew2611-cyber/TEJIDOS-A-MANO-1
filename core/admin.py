# core/admin.py - ¡VERSIÓN CORREGIDA!

from django.contrib import admin
# ¡IMPORTANTE! Solo importa los modelos que se definen en core/models.py
# Categoria y Producto NO deben importarse ni registrarse aquí.
from .models import Pedido, ItemPedido # <--- MODIFICADO AQUÍ. Se asume que Pedido e ItemPedido son los únicos modelos en core/models.py

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['producto', 'precio', 'cantidad']
    # Si quieres que el campo 'producto' sea un selector de búsqueda (útil con muchos productos)
    # raw_id_fields = ['producto']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_completo', 'email', 'total_pedido', 'estado', 'fecha_pedido', 'hecho_por_admin')
    list_filter = ('estado', 'fecha_pedido', 'hecho_por_admin')
    search_fields = ('id', 'nombre_completo', 'email', 'direccion_envio')
    inlines = [ItemPedidoInline]
    date_hierarchy = 'fecha_pedido'
    readonly_fields = ('fecha_pedido', 'total_pedido', 'usuario') # Asegúrate de que 'usuario' sea un campo que quieras solo de lectura

    actions = ['marcar_como_procesando', 'marcar_como_enviado', 'marcar_como_completado']

    def marcar_como_procesando(self, request, queryset):
        queryset.update(estado='procesando')
        self.message_user(request, "Pedidos seleccionados marcados como 'Procesando'.")
    marcar_como_procesando.short_description = "Marcar pedidos como Procesando"

    def marcar_como_enviado(self, request, queryset):
        queryset.update(estado='enviado')
        self.message_user(request, "Pedidos seleccionados marcados como 'Enviado'.")
    marcar_como_enviado.short_description = "Marcar pedidos como Enviado"

    def marcar_como_completado(self, request, queryset):
        queryset.update(estado='completado')
        self.message_user(request, "Pedidos seleccionados marcados como 'Completado'.")
    marcar_como_completado.short_description = "Marcar pedidos como Completado"

# --- ¡MUY IMPORTANTE! ---
# Las siguientes líneas son las que causaban el error 'AlreadyRegistered'.
# Categoria y Producto DEBEN ser registrados ÚNICAMENTE en productos/admin.py
# Por lo tanto, las ELIMINAMOS de core/admin.py
#
# @admin.register(Categoria)
# class CategoriaAdmin(admin.ModelAdmin):
#     list_display = ('nombre',)
#     search_fields = ('nombre',)
#
# @admin.register(Producto)
# class ProductoAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'categoria', 'precio', 'stock', 'disponible', 'fecha_creacion')
#     list_filter = ('categoria', 'disponible')
#     search_fields = ('nombre', 'descripcion')
#     list_editable = ('precio', 'stock', 'disponible')
#     raw_id_fields = ('categoria',)