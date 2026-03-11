from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('ruta/<int:id>/', views.detalle_ruta, name='detalle_ruta'), # <-- Nueva URL
]