from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('ruta/<int:id>/', views.detalle_ruta, name='detalle_ruta'), # <-- Nueva URL
    path('buscar/', views.buscar_ruta, name='buscar_ruta'),
    path('ruta/<int:ruta_id>/', views.detalle_ruta, name='detalle_ruta'),

    # User Story 04 - Combinación de Rutas
    path('buscador/', views.buscador_rutas, name='buscador_rutas'),
    path('calcular/', views.calcular_rutas_combinadas, name='calcular_rutas'),
    path('viaje/<int:viaje_id>/', views.detalle_viaje, name='detalle_viaje'),
    
]