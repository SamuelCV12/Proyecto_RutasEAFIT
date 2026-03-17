from django.contrib import admin
from .models import Lugar, Ruta

@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud', 'longitud')
    search_fields = ('nombre',)

@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'origen', 'destino', 'precio', 'tiempo_estimado_min')
    list_filter = ('origen', 'destino')
    search_fields = ('nombre',)