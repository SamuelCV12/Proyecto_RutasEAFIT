from django.shortcuts import render, get_object_or_404
from .models import Ruta

def buscar_ruta(request):
    rutas = []
    consulta = request.GET.get('destino', '')
    if consulta:
        rutas = Ruta.objects.filter(destino__icontains=consulta)
    return render(request, 'rutas/buscar.html', {
        'rutas': rutas,
        'consulta': consulta
    })

def detalle_ruta(request, ruta_id):
    ruta = get_object_or_404(Ruta, id=ruta_id)
    return render(request, 'rutas/detalle.html', {'ruta': ruta})