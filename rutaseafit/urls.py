from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conectamos las URLs de la app 'rutas'
    # Si quieres que la página de inicio sea el mapa, deja el primer string vacío ''
    path('', include('rutas.urls')), 
]