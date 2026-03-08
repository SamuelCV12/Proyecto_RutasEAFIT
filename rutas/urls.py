from django.urls import path
from . import views

urlpatterns = [
    path('buscar/', views.buscar_ruta, name='buscar_ruta'),
    path('ruta/<int:ruta_id>/', views.detalle_ruta, name='detalle_ruta'),
]