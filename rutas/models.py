from django.db import models

class Ruta(models.Model):
    nombre = models.CharField(max_length=100, help_text="Ej: Ruta Comercial Hotelera")
    origen = models.CharField(max_length=100, default="Universidad EAFIT")
    destino = models.CharField(max_length=100)
    tiempo_estimado_minutos = models.IntegerField(help_text="Duración aproximada en minutos")
    
    def __str__(self):
        return f"{self.nombre} ({self.origen} a {self.destino})"
