from django.urls import path
from . import views

app_name = 'rutas'
handler404 = 'rutas.views.error_404'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('inicio/', views.buscar_rutas, name='buscar_rutas'),
    path('ruta/<int:ruta_id>/', views.detalle_ruta, name='detalle_ruta'),
    
    # NUEVA RUTA PARA EL MAPA INTERACTIVO
    path('mapa/<int:ruta_id>/', views.mapa_ruta, name='mapa_ruta'),
]