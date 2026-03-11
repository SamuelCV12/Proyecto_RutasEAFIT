from django.shortcuts import render, get_object_or_404
from .models import Ruta
from django.db.models import Q

def inicio(request):
    origen_buscado = request.GET.get('origen', '')
    destino_buscado = request.GET.get('destino', '')
    sort_by = request.GET.get('sort', 'fastest')
    
    rutas = Ruta.objects.all()

    if origen_buscado or destino_buscado:
        rutas = rutas.filter(
            Q(origen__icontains=origen_buscado) & 
            Q(destino__icontains=destino_buscado)
        )
    
    # --- LA NUEVA LÓGICA DE TUS BOTONES ---
    if sort_by == 'fastest':
        # Ordena por tiempo y SOLO saca el primero (1 opción)
        rutas = rutas.order_by('tiempo_estimado_minutos', 'transbordos')[:1]
        
    elif sort_by == 'direct':
        # Filtra para que no haya transbordos (pueden ser varias opciones)
        rutas = rutas.filter(transbordos=0).order_by('tiempo_estimado_minutos')
        
    elif sort_by == 'cheapest':
        # Ordena por precio y SOLO saca el primero (1 opción)
        rutas = rutas.order_by('precio', 'tiempo_estimado_minutos')[:1]
        
    contexto = {
        'rutas': rutas,
        'origen_buscado': origen_buscado,
        'destino_buscado': destino_buscado,
        'sort_by': sort_by
    }
    return render(request, 'rutas/inicio.html', contexto)

def detalle_ruta(request, id):
    ruta = get_object_or_404(Ruta, id=id)
    lista_paradas = ruta.get_paradas_list()
    contexto = {
        'ruta': ruta,
        'lista_paradas': lista_paradas
    }
    return render(request, 'rutas/detalle.html', contexto)