from django.contrib import admin
from .models import (
    Ruta, Parada, RutaBus, HorarioParada, ViajeCompleto,
    Tramo, PuntoTransbordo, AdvertenciaRuta, AlternativaRuta
)

# Registro para el modelo de tus compañeros
@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'origen', 'destino', 'precio')

# Registro para tus modelos de la US04
@admin.register(Parada)
class ParadaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'barrio', 'latitud', 'longitud')

@admin.register(RutaBus)
class RutaBusAdmin(admin.ModelAdmin):
    list_display = ('numero_ruta', 'nombre', 'tarifa')

@admin.register(ViajeCompleto)
class ViajeCompletoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario_viaje', 'fecha_consulta', 'costo_total')

admin.site.register(Tramo)
admin.site.register(PuntoTransbordo)
admin.site.register(AdvertenciaRuta)
admin.site.register(AlternativaRuta)