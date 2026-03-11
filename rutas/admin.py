from django.contrib import admin
<<<<<<< HEAD
from .models import Ruta

admin.site.register(Ruta)
=======
from .models import (
    Parada, RutaBus, HorarioParada, ViajeCompleto,
    Tramo, PuntoTransbordo, AdvertenciaRuta, AlternativaRuta
)


@admin.register(Parada)
class ParadaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'barrio', 'latitud', 'longitud')
    search_fields = ('nombre', 'barrio')
    list_filter = ('barrio',)


@admin.register(RutaBus)
class RutaBusAdmin(admin.ModelAdmin):
    list_display = ('numero_ruta', 'nombre', 'origen', 'destino', 'tipo_servicio', 'tarifa', 'activa')
    search_fields = ('numero_ruta', 'nombre')
    list_filter = ('tipo_servicio', 'activa')
    ordering = ('numero_ruta',)


@admin.register(HorarioParada)
class HorarioParadaAdmin(admin.ModelAdmin):
    list_display = ('ruta', 'parada', 'hora_paso', 'orden', 'dias_operacion')
    search_fields = ('ruta__numero_ruta', 'parada__nombre')
    list_filter = ('dias_operacion', 'ruta')
    ordering = ('ruta', 'orden')


class TramoInline(admin.TabularInline):
    model = Tramo
    extra = 0
    fields = ('orden', 'tipo', 'ruta', 'parada_origen', 'parada_destino', 'hora_salida', 'hora_llegada')
    readonly_fields = ('orden',)


class AdvertenciaInline(admin.TabularInline):
    model = AdvertenciaRuta
    extra = 0
    fields = ('tipo_advertencia', 'mensaje', 'severidad')


@admin.register(ViajeCompleto)
class ViajeCompletoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario_viaje', 'fecha_consulta', 'duracion_total_minutos', 'costo_total', 'numero_transbordos', 'estado')
    search_fields = ('usuario_viaje__username',)
    list_filter = ('estado', 'fecha_consulta')
    ordering = ('-fecha_consulta',)
    inlines = [TramoInline, AdvertenciaInline]
    
    fieldsets = (
        ('Usuario', {
            'fields': ('usuario_viaje',)
        }),
        ('Ubicaciones', {
            'fields': (('origen_latitud', 'origen_longitud'), ('destino_latitud', 'destino_longitud'))
        }),
        ('Detalles del Viaje', {
            'fields': ('duracion_total_minutos', 'costo_total', 'numero_transbordos', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_consulta', 'fecha_viaje_planeado')
        }),
    )


@admin.register(Tramo)
class TramoAdmin(admin.ModelAdmin):
    list_display = ('viaje', 'orden', 'tipo', 'ruta', 'parada_origen', 'parada_destino', 'duracion_minutos')
    search_fields = ('viaje__id', 'ruta__numero_ruta')
    list_filter = ('tipo',)
    ordering = ('viaje', 'orden')


@admin.register(PuntoTransbordo)
class PuntoTransbordoAdmin(admin.ModelAdmin):
    list_display = ('tramo', 'parada', 'tiempo_espera_minutos', 'distancia_caminata_metros', 'ruta_origen', 'ruta_destino')
    search_fields = ('parada__nombre', 'ruta_origen__numero_ruta', 'ruta_destino__numero_ruta')


@admin.register(AdvertenciaRuta)
class AdvertenciaRutaAdmin(admin.ModelAdmin):
    list_display = ('viaje', 'tipo_advertencia', 'severidad', 'fecha_creacion')
    search_fields = ('viaje__id',)
    list_filter = ('tipo_advertencia', 'severidad', 'fecha_creacion')
    ordering = ('-fecha_creacion',)


@admin.register(AlternativaRuta)
class AlternativaRutaAdmin(admin.ModelAdmin):
    list_display = ('viaje_original', 'orden_prioridad', 'ventaja')
    search_fields = ('viaje_original__id',)
    ordering = ('viaje_original', 'orden_prioridad')
>>>>>>> origin/MariaLauraTafurGomez
