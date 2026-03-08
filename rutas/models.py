from django.db import models
from django.contrib.auth.models import User

class Parada(models.Model):
    nombre = models.CharField(max_length=150)
    latitud = models.FloatField()
    longitud = models.FloatField()
    barrio = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'rutas'
        verbose_name = "Parada"
        verbose_name_plural = "Paradas"
    
    def __str__(self):
        return self.nombre

class RutaBus(models.Model):
    numero_ruta = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=150)
    origen = models.CharField(max_length=150)
    destino = models.CharField(max_length=150)
    tipo_servicio = models.CharField(max_length=20, default='estandar')
    tarifa = models.DecimalField(max_digits=10, decimal_places=2) # Aumentado por si acaso
    tiempo_estimado_minutos = models.IntegerField()
    activa = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'rutas'

    def __str__(self):
        return self.numero_ruta

class HorarioParada(models.Model):
    ruta = models.ForeignKey('RutaBus', on_delete=models.CASCADE, related_name='horarios')
    parada = models.ForeignKey('Parada', on_delete=models.CASCADE, related_name='horarios')
    hora_paso = models.TimeField()
    orden = models.IntegerField()
    dias_operacion = models.CharField(max_length=20, default='LUN-VIE')
    
    class Meta:
        app_label = 'rutas'

class ViajeCompleto(models.Model):
    usuario_viaje = models.ForeignKey(
      User, on_delete=models.CASCADE, null=True, blank=True
      )
    origen_latitud = models.FloatField()
    origen_longitud = models.FloatField()
    destino_latitud = models.FloatField()
    destino_longitud = models.FloatField()
    duracion_total_minutos = models.IntegerField()
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)
    numero_transbordos = models.IntegerField(default=0)
    fecha_consulta = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='valido')
    
    class Meta:
        app_label = 'rutas'

class Tramo(models.Model):
    viaje = models.ForeignKey('ViajeCompleto', on_delete=models.CASCADE, related_name='tramos')
    orden = models.IntegerField()
    tipo = models.CharField(max_length=20) # 'bus' o 'transbordo'
    ruta = models.ForeignKey('RutaBus', on_delete=models.SET_NULL, null=True, blank=True)
    parada_origen = models.ForeignKey('Parada', on_delete=models.SET_NULL, null=True, related_name='tramos_origen')
    parada_destino = models.ForeignKey('Parada', on_delete=models.SET_NULL, null=True, related_name='tramos_destino')
    hora_salida = models.TimeField()
    hora_llegada = models.TimeField()
    duracion_minutos = models.IntegerField()
    # --- VARIABLES AGREGADAS PARA CORREGIR ERROR ---
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    instrucciones = models.TextField(blank=True, null=True) 
    
    class Meta:
        app_label = 'rutas'

class PuntoTransbordo(models.Model):
    tramo = models.OneToOneField('Tramo', on_delete=models.CASCADE, related_name='transbordo')
    parada = models.ForeignKey('Parada', on_delete=models.CASCADE)
    tiempo_espera_minutos = models.IntegerField()
    distancia_caminata_metros = models.IntegerField(default=0)
    ruta_origen = models.ForeignKey('RutaBus', on_delete=models.SET_NULL, null=True, related_name='trans_origen')
    ruta_destino = models.ForeignKey('RutaBus', on_delete=models.SET_NULL, null=True, related_name='trans_dest')
    # --- VARIABLE AGREGADA PARA GUARDAR DETALLE ---
    instrucciones_detalladas = models.TextField(blank=True, null=True) 

    class Meta:
        app_label = 'rutas'

class AdvertenciaRuta(models.Model):
    viaje = models.ForeignKey('ViajeCompleto', on_delete=models.CASCADE, related_name='advertencias')
    tipo_advertencia = models.CharField(max_length=30)
    mensaje = models.TextField()
    severidad = models.CharField(max_length=10, default='media')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'rutas'

class AlternativaRuta(models.Model):
    viaje_original = models.ForeignKey('ViajeCompleto', on_delete=models.CASCADE, related_name='alternativas')
    descripcion = models.TextField()
    ventaja = models.CharField(max_length=200)
    orden_prioridad = models.IntegerField(default=1)
    
    class Meta:
        app_label = 'rutas'