from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Min, Count
from datetime import datetime, timedelta, time
import json

from .models import (
    RutaBus, Parada, HorarioParada, ViajeCompleto, 
    Tramo, PuntoTransbordo, AdvertenciaRuta, AlternativaRuta
)

# ============================================
# VISTAS PARA USER STORY 04
# ============================================

def buscador_rutas(request):
    """Vista principal del buscador de rutas combinadas"""
    destinos_populares = [
        {'nombre': 'San Diego Mall', 'lat': 6.230833, 'lng': -75.590556},
        {'nombre': 'Parque Lleras', 'lat': 6.208419, 'lng': -75.568466},
        {'nombre': 'El Poblado', 'lat': 6.210833, 'lng': -75.571389},
        {'nombre': 'Centro Comercial El Tesoro', 'lat': 6.196111, 'lng': -75.562222},
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
@require_http_methods(["POST"])
@require_http_methods(["POST"])
def calcular_rutas_combinadas(request):
    """
    Calcula, guarda en DB TODAS las opciones encontradas y las retorna.
    Maneja el usuario como opcional y asegura que cada ruta tenga su viaje_id.
    """
    try:
        # 1. Cargar datos del mapa (Frontend)
        data = json.loads(request.body)
        origen_lat = float(data.get('origen_lat'))
        origen_lng = float(data.get('origen_lng'))
        destino_lat = float(data.get('destino_lat'))
        destino_lng = float(data.get('destino_lng'))
        preferencia = data.get('preferencia', 'mas_rapido')
        
        # 2. Encontrar paradas cercanas
        parada_origen = encontrar_parada_cercana(origen_lat, origen_lng)
        parada_destino = encontrar_parada_cercana(destino_lat, destino_lng)
        
        if not parada_origen or not parada_destino:
            return JsonResponse({
                'success': False, 
                'error': 'No se encontraron paradas cercanas al origen o destino'
            }, status=400)
        
        # 3. Calcular la lógica de rutas
        rutas_encontradas = calcular_rutas_con_transbordos(
            parada_origen, 
            parada_destino, 
            preferencia
        )
        
        if rutas_encontradas:
            usuario_actual = request.user if request.user.is_authenticated else None
            rutas_formateadas = []
            
            # --- GUARDADO MASIVO EN DB ---
            # Tomamos hasta las primeras 5 rutas para no saturar, pero guardamos cada una
            for idx, ruta_data in enumerate(rutas_encontradas[:5]):
                viaje_id = None
                try:
                    # Guardamos el registro real en la base de datos
                    # Asegúrate de que guardar_viaje_en_bd use 'usuario_viaje' internamente
                    viaje_db = guardar_viaje_en_bd(
                        usuario_actual, 
                        origen_lat, origen_lng,
                        destino_lat, destino_lng,
                        ruta_data
                    )
                    viaje_id = viaje_db.id
                except Exception as db_error:
                    # Si falla el guardado de una, logueamos pero seguimos con la siguiente
                    print(f"Error guardando ruta alternativa {idx}: {db_error}")
                
                # Formateamos la ruta incluyendo su ID único de base de datos
                ruta_dict = formatear_ruta_para_respuesta(ruta_data, viaje_id)
                rutas_formateadas.append(ruta_dict)
            
            # 4. Respuesta al Frontend
            return JsonResponse({
                'success': True,
                'rutas': rutas_formateadas,
                'total_opciones': len(rutas_encontradas),
                'viaje_id_principal': rutas_formateadas[0]['viaje_id'] if rutas_formateadas else None
            })
            
        else:
            return JsonResponse({
                'success': False, 
                'error': 'No pudimos encontrar una combinación de buses para esta ruta'
            }, status=404)
            
    except Exception as e:
        print(f"ERROR CRÍTICO EN CALCULAR_RUTAS: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': f'Error interno del servidor: {str(e)}'
        }, status=500)
def encontrar_parada_cercana(lat, lng, radio_km=0.5):
    delta = radio_km / 111.0
    paradas = Parada.objects.filter(
        latitud__gte=lat - delta, latitud__lte=lat + delta,
        longitud__gte=lng - delta, longitud__lte=lng + delta
    )
    return paradas.first() if paradas.exists() else None

def calcular_rutas_con_transbordos(parada_origen, parada_destino, preferencia='mas_rapido'):
    rutas_posibles = []
    rutas_posibles.extend(buscar_rutas_directas(parada_origen, parada_destino))
    rutas_posibles.extend(buscar_rutas_con_transbordo(parada_origen, parada_destino, max_transbordos=1))
    
    if len(rutas_posibles) < 3:
        rutas_posibles.extend(buscar_rutas_con_transbordo(parada_origen, parada_destino, max_transbordos=2))
    
    if preferencia == 'mas_rapido':
        rutas_posibles.sort(key=lambda r: r['duracion_total'])
    elif preferencia == 'mas_barato':
        rutas_posibles.sort(key=lambda r: r['costo_total'])
    elif preferencia == 'menos_transbordos':
        rutas_posibles.sort(key=lambda r: r['numero_transbordos'])
    
    return rutas_posibles

def buscar_rutas_directas(parada_origen, parada_destino):
    rutas = []
    horarios_origen = HorarioParada.objects.filter(parada=parada_origen)
    for h_origen in horarios_origen:
        ruta = h_origen.ruta
        horarios_destino = HorarioParada.objects.filter(ruta=ruta, parada=parada_destino, orden__gt=h_origen.orden)
        if horarios_destino.exists():
            h_destino = horarios_destino.first()
            duracion = calcular_duracion(h_origen.hora_paso, h_destino.hora_paso)
            rutas.append({
                'tipo': 'directa',
                'tramos': [{
                    'tipo': 'bus', 'ruta': ruta, 'parada_origen': parada_origen, 'parada_destino': parada_destino,
                    'hora_salida': h_origen.hora_paso, 'hora_llegada': h_destino.hora_paso, 'duracion': duracion,
                    'instrucciones': f"Tomar bus {ruta.numero_ruta} en {parada_origen.nombre}"
                }],
                'duracion_total': duracion, 'costo_total': float(ruta.tarifa), 'numero_transbordos': 0,
                'advertencias': [], 'estado': 'valido'
            })
    return rutas

def buscar_rutas_con_transbordo(parada_origen, parada_destino, max_transbordos=1):
    rutas = []
    horarios_desde_origen = HorarioParada.objects.filter(parada=parada_origen).select_related('ruta')
    for h_origen in horarios_desde_origen:
        ruta_1 = h_origen.ruta
        paradas_intermedias = HorarioParada.objects.filter(ruta=ruta_1, orden__gt=h_origen.orden).select_related('parada')[:10]
        for h_intermedia in paradas_intermedias:
            parada_transbordo = h_intermedia.parada
            horarios_desde_transbordo = HorarioParada.objects.filter(parada=parada_transbordo).exclude(ruta=ruta_1).select_related('ruta')
            for h_transbordo in horarios_desde_transbordo:
                ruta_2 = h_transbordo.ruta
                horarios_destino = HorarioParada.objects.filter(ruta=ruta_2, parada=parada_destino, orden__gt=h_transbordo.orden)
                if horarios_destino.exists():
                    h_destino = horarios_destino.first()
                    tiempo_espera = calcular_tiempo_espera(h_intermedia.hora_paso, h_transbordo.hora_paso)
                    es_valido, advertencias = validar_transbordo(tiempo_espera)
                    duracion_1 = calcular_duracion(h_origen.hora_paso, h_intermedia.hora_paso)
                    duracion_2 = calcular_duracion(h_transbordo.hora_paso, h_destino.hora_paso)
                    
                    rutas.append({
                        'tipo': 'con_transbordo',
                        'tramos': [
                            {'tipo': 'bus', 'ruta': ruta_1, 'parada_origen': parada_origen, 'parada_destino': parada_transbordo, 'hora_salida': h_origen.hora_paso, 'hora_llegada': h_intermedia.hora_paso, 'duracion': duracion_1, 'instrucciones': f"Tomar bus {ruta_1.numero_ruta}"},
                            {'tipo': 'transbordo', 'parada': parada_transbordo, 'tiempo_espera': tiempo_espera, 'ruta_origen': ruta_1, 'ruta_destino': ruta_2, 'instrucciones': f"Transbordo en {parada_transbordo.nombre}"},
                            {'tipo': 'bus', 'ruta': ruta_2, 'parada_origen': parada_transbordo, 'parada_destino': parada_destino, 'hora_salida': h_transbordo.hora_paso, 'hora_llegada': h_destino.hora_paso, 'duracion': duracion_2, 'instrucciones': f"Tomar bus {ruta_2.numero_ruta}"}
                        ],
                        'duracion_total': duracion_1 + tiempo_espera + duracion_2,
                        'costo_total': float(ruta_1.tarifa + ruta_2.tarifa),
                        'numero_transbordos': 1, 'advertencias': advertencias, 'estado': 'valido' if es_valido else 'conflicto'
                    })
    return rutas[:10]

def validar_transbordo(tiempo_espera):
    advertencias = []
    es_valido = True
    if tiempo_espera < 5:
        advertencias.append({'tipo': 'tiempo_insuficiente', 'mensaje': 'Tiempo muy ajustado', 'severidad': 'alta'})
        es_valido = False
    return es_valido, advertencias

def calcular_duracion(inicio, fin):
    if isinstance(inicio, time) and isinstance(fin, time):
        i = timedelta(hours=inicio.hour, minutes=inicio.minute)
        f = timedelta(hours=fin.hour, minutes=fin.minute)
        return int(((f - i).total_seconds() / 60)) if f > i else int(((timedelta(days=1) - i + f).total_seconds() / 60))
    return 0

def calcular_tiempo_espera(llegada, salida):
    return calcular_duracion(llegada, salida)

def guardar_viaje_en_bd(usuario, origen_lat, origen_lng, destino_lat, destino_lng, ruta_data):
    """
    Guarda el viaje de forma segura. 
    Asegúrate de que 'usuario' pueda ser None en tu models.py.
    """
    # 1. Crear el viaje principal
    viaje = ViajeCompleto.objects.create(
        usuario_viaje=usuario, 
        origen_latitud=origen_lat,
        origen_longitud=origen_lng,
        destino_latitud=destino_lat,
        destino_longitud=destino_lng,
        duracion_total_minutos=ruta_data.get('duracion_total', 0),
        costo_total=ruta_data.get('costo_total', 0),
        numero_transbordos=ruta_data.get('numero_transbordos', 0),
        estado=ruta_data.get('estado', 'valido')
    )
    
    # 2. Guardar cada tramo
    for idx, t in enumerate(ruta_data.get('tramos', []), start=1):
        # Verificamos que los objetos existan antes de asignarlos
        ruta_obj = t.get('ruta') if hasattr(t.get('ruta'), 'pk') else None
        p_origen = t.get('parada_origen') if hasattr(t.get('parada_origen'), 'pk') else None
        p_destino = t.get('parada_destino') if hasattr(t.get('parada_destino'), 'pk') else None

        tramo = Tramo.objects.create(
            viaje=viaje,
            orden=idx,
            tipo=t.get('tipo', 'bus'),
            ruta=ruta_obj,
            parada_origen=p_origen,
            parada_destino=p_destino,
            hora_salida=t.get('hora_salida', time(0,0)),
            hora_llegada=t.get('hora_llegada', time(0,0)),
            duracion_minutos=t.get('duracion', 0),
            instrucciones=t.get('instrucciones', '')
        )
        
        # 3. Guardar transbordo si aplica
        if t.get('tipo') == 'transbordo':
            PuntoTransbordo.objects.create(
                tramo=tramo,
                parada=t.get('parada') if hasattr(t.get('parada'), 'pk') else None,
                tiempo_espera_minutos=t.get('tiempo_espera', 0),
                instrucciones_detalladas=t.get('instrucciones', '')
            )
    return viaje
def formatear_ruta_para_respuesta(ruta_data, viaje_id=None):
    tramos = ruta_data.get('tramos', [])
    advertencias = []
    alternativas_sugeridas = []

    # Lógica de detección de falla
    for tramo in tramos:
        if tramo.get('tipo') == 'transbordo':
            # Simulamos o verificamos incompatibilidad (ej: espera > 15 min)
            if tramo.get('tiempo_espera', 0) > 15:
                advertencias.append({
                    'tipo': 'retraso_probable',
                    'mensaje': 'Conexión lenta detectada. Buscando alternativas...',
                    'severidad': 'media'
                })
                
                # BUSCAMOS LA ALTERNATIVA REAL EN LA DB
                parada_actual = tramo.get('parada_id') # Asegúrate de tener este ID
                destino_id = ruta_data.get('destino_id')
                
                alternativas_sugeridas = buscar_alternativas_desde_parada(parada_actual, destino_id)
    return {
        'viaje_id': viaje_id,
        'duracion_total': f"{ruta_data['duracion_total']} min",
        'costo_total': f"${ruta_data['costo_total']:,.0f} COP",
        'numero_transbordos': ruta_data['numero_transbordos'],
        'estado': ruta_data.get('estado', 'valido'),
        'tramos': [
            {
                'tipo': t['tipo'],
                # Usamos .get() y validamos si existe el objeto ruta para evitar errores
                'ruta': t.get('ruta').numero_ruta if t.get('ruta') else "Caminata/Transbordo",
                'origen': t.get('parada_origen').nombre if t.get('parada_origen') else "Origen",
                'destino': t.get('parada_destino').nombre if t.get('parada_destino') else "Destino",
                'hora_salida': t.get('hora_salida').strftime('%H:%M') if hasattr(t.get('hora_salida'), 'strftime') else "N/A",
                'hora_llegada': t.get('hora_llegada').strftime('%H:%M') if hasattr(t.get('hora_llegada'), 'strftime') else "N/A",
                'instrucciones': t['instrucciones']
            }
            for t in ruta_data['tramos']
        ],
        'advertencias': ruta_data.get('advertencias', []),
        'alternativas_sugeridas': alternativas_sugeridas
    }
def detalle_viaje(request, viaje_id):
    viaje = get_object_or_404(ViajeCompleto, id=viaje_id)
    return render(request, 'rutas/detalle_viaje.html', {
        'viaje': viaje, 
        'tramos': viaje.tramos.all(), 
        'advertencias': viaje.advertencias.all()
    })

def buscar_alternativas_desde_parada(parada_id, destino_final_id):
    """
    Busca rutas que salgan desde la parada donde el usuario 
    quedó 'varado' hacia su destino final.
    """
    # Buscamos tramos que salgan de la parada actual
    alternativas = TramoRuta.objects.filter(
        parada_origen_id=parada_id,
        parada_destino_id=destino_final_id
    ).select_related('ruta')

    sugerencias = []
    for alt in alternativas:
        sugerencias.append({
            'nombre_ruta': alt.ruta.nombre,
            'mensaje': f"Alternativa viable: Toma la ruta {alt.ruta.nombre} (Costo: {alt.costo})",
            'tiempo_estimado': alt.tiempo_estimado_minutos
        })
    return sugerencias