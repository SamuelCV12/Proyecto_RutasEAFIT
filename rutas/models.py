from django.db import models

class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    # Agregamos coordenadas reales. Por defecto ponemos EAFIT para evitar errores con datos viejos.
    latitud = models.FloatField(default=6.2006, help_text="Ejemplo: 6.2006 (Usar punto para decimales)")
    longitud = models.FloatField(default=-75.5784, help_text="Ejemplo: -75.5784")

    def __str__(self):
        return self.nombre

class Ruta(models.Model):
    nombre = models.CharField(max_length=100, help_text="Ej: Poblado 134, Metro, etc.")
    origen = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='rutas_origen')
    destino = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='rutas_destino')
    precio = models.IntegerField(help_text="Precio en COP")
    tiempo_estimado_min = models.IntegerField(help_text="Tiempo en minutos")
    
    # Campo para guardar las paradas reales separadas por comas
    paradas_intermedias = models.TextField(
        blank=True, 
        help_text="Nombres separados por comas. Ej: Av Las Vegas, Estación Poblado, Milla de Oro"
    )

    def __str__(self):
        return f"{self.nombre} ({self.origen.nombre} -> {self.destino.nombre})"

    # Esta función convierte el texto separado por comas en una lista de Python
    def get_paradas_list(self):
        if self.paradas_intermedias:
            return [p.strip() for p in self.paradas_intermedias.split(',')]
        return []