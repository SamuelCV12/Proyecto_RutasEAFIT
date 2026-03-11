from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include # <-- Agrega 'include' aquí

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rutas.urls')), # <-- Conecta la app rutas a la página principal
]
=======
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rutas/', include('rutas.urls')),
]
>>>>>>> origin/AnaSofiaAngaritaBarrios
