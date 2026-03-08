from django.apps import AppConfig
import sys

class RutasEAFITConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rutasEAFIT'
    path = '/app' # Ruta dentro del contenedor

    def ready(self):
        # Esto es lo que hace la magia:
        try:
            import rutas.models as models 
        except ImportError:
            pass