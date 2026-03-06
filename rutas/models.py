import re
from django.db import models

class Ruta(models.Model):
    nombre = models.CharField(max_length=100, help_text="Ej: Integrado Metro 132i")
    origen = models.CharField(max_length=100, help_text="Punto de partida del usuario")
    destino = models.CharField(max_length=100, default="Universidad EAFIT")
    tiempo_estimado_minutos = models.IntegerField(help_text="Duración aproximada en minutos")
    paradas = models.TextField(default="Sin especificar", help_text="Separadas por coma. Ej: Estación Poblado, Av. Las Vegas, EAFIT")
    transbordos = models.IntegerField(default=0, help_text="Cantidad de transbordos (0 = Ruta directa)")
    
    # NUEVO CAMPO: Precio
    precio = models.IntegerField(default=3200, help_text="Precio en COP")
    
    def __str__(self):
        return f"{self.nombre} ({self.origen} a {self.destino})"
        
    # Esta pequeña función convierte el texto de paradas en una lista para dibujar la línea de tiempo
    def get_paradas_list(self):
        # Esto divide el texto automáticamente si usas comas O números (ej. "1. ", "2. ")
        lista = re.split(r',\s*|\s*\d+\.\s*', self.paradas)
        # Limpiamos los espacios y quitamos los pedazos vacíos
        return [p.strip() for p in lista if p.strip()]