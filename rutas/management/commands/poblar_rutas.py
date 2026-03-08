from django.core.management.base import BaseCommand
from rutas.models import Ruta

class Command(BaseCommand):
    help = 'Pobla la base de datos con rutas de prueba'

    def handle(self, *args, **kwargs):
        Ruta.objects.all().delete()
        rutas = [
            Ruta(nombre='Ruta Hospital', origen='Universidad EAFIT', destino='Hospital Pablo Tobón Uribe', tiempo_estimado_minutos=20),
            Ruta(nombre='Ruta Centro', origen='Universidad EAFIT', destino='Centro de Medellín', tiempo_estimado_minutos=35),
            Ruta(nombre='Ruta Poblado', origen='Universidad EAFIT', destino='El Poblado', tiempo_estimado_minutos=15),
            Ruta(nombre='Ruta Laureles', origen='Universidad EAFIT', destino='Laureles', tiempo_estimado_minutos=25),
            Ruta(nombre='Ruta Aeropuerto', origen='Universidad EAFIT', destino='Aeropuerto Olaya Herrera', tiempo_estimado_minutos=40),
        ]
        Ruta.objects.bulk_create(rutas)
        self.stdout.write(self.style.SUCCESS('✅ Rutas creadas exitosamente'))