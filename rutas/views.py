from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Min, Count
from datetime import datetime, timedelta, time
import json

# Importación unificada de todos los modelos de ambas ramas
from .models import (
    Ruta, RutaBus, Parada, HorarioParada, ViajeCompleto, 
    Tramo, PuntoTransbordo, AdvertenciaRuta, AlternativaRuta
)

# ============================================
# VISTAS DE BÚSQUEDA SIMPLE (Samuel / Ana)
# ============================================

def inicio(request):
    """Buscador básico de la página principal"""
    origen_buscado = request.GET.get('origen', '')
    destino_buscado = request.GET.get('destino', '')
    sort_by = request.GET.get('sort', 'fastest')
    
    rutas = Ruta.objects.all()

    if origen_buscado or destino_buscado:
        rutas = rutas.filter(
            Q(origen__icontains=origen_buscado) & 
            Q(destino__icontains=destino_buscado)
        )
    
    if sort_by == 'fastest':
        rutas = rutas.order_by('tiempo_estimado_minutos', 'transbordos')[:1]
    elif sort_by == 'direct':
        rutas = rutas.filter(transbordos=0).order_by('tiempo_estimado_minutos')
    elif sort_by == 'cheapest':
        rutas = rutas.order_by('precio', 'tiempo_estimado_minutos')[:1]
        
    contexto = {
        'rutas': rutas,
        'origen_buscado': origen_buscado,
        'destino_buscado': destino_buscado,
        'sort_by': sort_by
    }
    return render(request, 'rutas/inicio.html', contexto)

def buscar_ruta(request):
    """Vista de resultados para búsqueda por destino"""
    rutas = []
    consulta = request.GET.get('destino', '')
    if consulta:
        rutas = Ruta.objects.filter(destino__icontains=consulta)
    return render(request, 'rutas/buscar.html', {
        'rutas': rutas,
        'consulta': consulta
    })

def detalle_ruta(request, id):
    """Detalle de un bus individual (Ruta simple)"""
    ruta = get_object_or_404(Ruta, id=id)
    lista_paradas = ruta.get_paradas_list()
    contexto = {
        'ruta': ruta,
        'lista_paradas': lista_paradas
    }
    return render(request, 'rutas/detalle.html', contexto)

# ============================================
# VISTAS DE RUTAS COMBINADAS (Maria Laura - US04)
# ============================================

def buscador_rutas(request):
    """Vista principal con mapa y destinos de Medellín"""
    destinos_populares = [
        {'nombre': 'San Diego Mall', 'lat': 6.230833, 'lng': -75.590556},
        {'nombre': 'Parque Lleras', 'lat': 6.208419, 'lng': -75.568466},
        {'nombre': 'El Poblado', 'lat': 6.210833, 'lng': -75.571389},
        {'nombre': 'CC El Tesoro', 'lat': 6.196111, 'lng': -75.562222},
    ]
    paradas = Parada.objects.all()[:50] 
    context = {
        'destinos_populares': destinos_populares,
        'paradas': paradas,
        'origen_default': 'Universidad EAFIT',
        'origen_lat': 6.200663,
        'origen_lng': -75.578876
    }
    return render(request, 'rutas/buscador_rutas.html', context)

@require_http_methods(["POST"])
def calcular_rutas_combinadas(request):
    """Cálculo lógico de transbordos y guardado en DB"""
    try:
        data = json.loads(request.body)
        origen_lat = float(data.get('origen_lat'))
        origen_lng = float(data.get('origen_lng'))
        destino_lat = float(data.get('destino_lat'))
        destino_lng = float(data.get('destino_lng'))
        preferencia = data.get('preferencia', 'mas_rapido')
        
        parada_origen = encontrar_parada_cercana(origen_lat, origen_lng)
        parada_destino = encontrar_parada_cercana(destino_lat, destino_lng)
        
        if not parada_origen or not parada_destino:
            return JsonResponse({'success': False, 'error': 'No se encontraron paradas cercanas'}, status=400)
        
        rutas_encontradas = calcular_rutas_con_transbordos(parada_origen, parada_destino, preferencia)
        
        if rutas_encontradas:
            usuario_actual = request.user if request.user.is_authenticated else None
            rutas_formateadas = []
            
            for idx, ruta_data in enumerate(rutas_encontradas[:5]):
                viaje_db = guardar_viaje_en_bd(usuario_actual, origen_lat, origen_lng, destino_lat, destino_lng, ruta_data)
                rutas_formateadas.append(formatear_ruta_para_respuesta(ruta_data, viaje_db.id))
            
            return JsonResponse({
                'success': True,
                'rutas': rutas_formateadas,
                'total_opciones': len(rutas_encontradas),
                'viaje_id_principal': rutas_formateadas[0]['viaje_id'] if rutas_formateadas else None
            })
        return JsonResponse({'success': False, 'error': 'Sin combinaciones disponibles'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def detalle_viaje(request, viaje_id):
    """Vista detallada de un viaje complejo con tramos"""
    viaje = get_object_or_404(ViajeCompleto, id=viaje_id)
    return render(request, 'rutas/detalle_viaje.html', {
        'viaje': viaje, 
        'tramos': viaje.tramos.all(), 
        'advertencias': viaje.advertencias.all()
    })

# ============================================
# FUNCIONES AUXILIARES DE LÓGICA (Maria Laura)
# ============================================

def encontrar_parada_cercana(lat, lng, radio_km=0.5):
    delta = radio_km / 111.0
    paradas = Parada.objects.filter(
        latitud__gte=lat - delta, latitud__lte=lat + delta,
        longitud__gte=lng - delta, longitud__lte=lng + delta
    )
    return paradas.first()

def calcular_rutas_con_transbordos(parada_origen, parada_destino, preferencia='mas_rapido'):
    rutas_posibles = []
    rutas_posibles.extend(buscar_rutas_directas(parada_origen, parada_destino))
    rutas_posibles.extend(buscar_rutas_con_transbordo(parada_origen, parada_destino, max_transbordos=1))
    
    if preferencia == 'mas_rapido':
        rutas_posibles.sort(key=lambda r: r['duracion_total'])
    elif preferencia == 'mas_barato':
        rutas_posibles.sort(key=lambda r: r['costo_total'])
    return rutas_posibles

def buscar_rutas_directas(parada_origen, parada_destino):
    rutas = []
    horarios_origen = HorarioParada.objects.filter(parada=parada_origen)
    for h_origen in horarios_origen:
        ruta = h_origen.ruta
        h_destino = HorarioParada.objects.filter(ruta=ruta, parada=parada_destino, orden__gt=h_origen.orden).first()
        if h_destino:
            duracion = calcular_duracion(h_origen.hora_paso, h_destino.hora_paso)
            rutas.append({
                'tipo': 'directa',
                'tramos': [{
                    'tipo': 'bus', 'ruta': ruta, 'parada_origen': parada_origen, 'parada_destino': parada_destino,
                    'hora_salida': h_origen.hora_paso, 'hora_llegada': h_destino.hora_paso, 'duracion': duracion,
                    'instrucciones': f"Tomar bus {ruta.nombre} en {parada_origen.nombre}"
                }],
                'duracion_total': duracion, 'costo_total': float(ruta.precio), 'numero_transbordos': 0
            })
    return rutas

def buscar_rutas_con_transbordo(parada_origen, parada_destino, max_transbordos=1):
    rutas = []
    # Lógica simplificada para el merge
    return rutas 

def calcular_duracion(inicio, fin):
    if isinstance(inicio, time) and isinstance(fin, time):
        i = timedelta(hours=inicio.hour, minutes=inicio.minute)
        f = timedelta(hours=fin.hour, minutes=fin.minute)
        return int(((f - i).total_seconds() / 60)) if f > i else int(((timedelta(days=1) - i + f).total_seconds() / 60))
    return 0

def guardar_viaje_en_bd(usuario, origen_lat, origen_lng, destino_lat, destino_lng, ruta_data):
    viaje = ViajeCompleto.objects.create(
        usuario_viaje=usuario, origen_latitud=origen_lat, origen_longitud=origen_lng,
        destino_latitud=destino_lat, destino_longitud=destino_lng,
        duracion_total_minutos=ruta_data.get('duracion_total', 0),
        costo_total=ruta_data.get('costo_total', 0),
        numero_transbordos=ruta_data.get('numero_transbordos', 0)
    )
    return viaje

def formatear_ruta_para_respuesta(ruta_data, viaje_id):
    return {
        'viaje_id': viaje_id,
        'duracion_total': f"{ruta_data['duracion_total']} min",
        'costo_total': f"${ruta_data['costo_total']}",
        'numero_transbordos': ruta_data['numero_transbordos'],
        'tramos': []
    }