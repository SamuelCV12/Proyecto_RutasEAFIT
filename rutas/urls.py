from django.urls import path
from . import views  # El punto '.' significa "esta misma carpeta"

app_name = 'rutas'

urlpatterns = [
    # User Story 04 - Combinación de Rutas
    path('buscador/', views.buscador_rutas, name='buscador_rutas'),
    path('calcular/', views.calcular_rutas_combinadas, name='calcular_rutas'),
    path('viaje/<int:viaje_id>/', views.detalle_viaje, name='detalle_viaje'),
    
]