from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Aquí le decimos a Django que incluya todas las URLs de nuestra app
    path('', include('rutas.urls')),
]