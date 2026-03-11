from django.urls import path
from . import views

urlpatterns = [
    # --- Vistas de Samuel / Ana (Buscador Simple) ---
    path('', views.inicio, name='inicio'),
    path('buscar/', views.buscar_ruta, name='buscar_ruta'),
    path('ruta/<int:ruta_id>/', views.detalle_ruta, name='detalle_ruta'),

    # --- User Story 04 - Maria Laura (Combinación de Rutas/Transbordos) ---
    path('buscador/', views.buscador_rutas, name='buscador_rutas'),
    path('calcular/', views.calcular_rutas_combinadas, name='calcular_rutas'),
    path('viaje/<int:viaje_id>/', views.detalle_viaje, name='detalle_viaje'),
]