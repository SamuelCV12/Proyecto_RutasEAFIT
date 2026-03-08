from django.urls import path
from . import views

app_name = 'routes'

urlpatterns = [
    path('', views.route_list, name='route_list'),
    path('route/<int:route_id>/guide/', views.route_guide, name='route_guide'),
]
