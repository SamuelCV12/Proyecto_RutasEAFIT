from django.shortcuts import render, get_object_or_404, redirect
from .models import Lugar, Ruta
from datetime import datetime, timedelta
import json

# --- VISTAS DE AUTENTICACIÓN ---
# (Nota: Estas se conectarán a la lógica real en el Paso 1 de Autenticación)
def login_view(request):
    return render(request, 'rutas/login.html')

def registro_view(request):
    return render(request, 'rutas/registro.html')

# --- VISTA PRINCIPAL (BUSCADOR) con Robustez ---
def buscar_rutas(request):
    lugares = Lugar.objects.all()
    rutas_directas = []
    rutas_transbordo = []
    origen_seleccionado = None
    destino_seleccionado = None
    busqueda_realizada = False
    error_message = None # Variable para manejar errores de usuario
    
    filtro_actual = request.GET.get('filtro', 'todas')

    if 'origen' in request.GET and 'destino' in request.GET:
        origen_id = request.GET.get('origen')
        destino_id = request.GET.get('destino')

        # VALIDACIÓN DE ROBUSTEZ: Origen y destino iguales
        if origen_id == destino_id:
            error_message = "El origen y el destino no pueden ser el mismo lugar."
        elif origen_id and destino_id:
            busqueda_realizada = True
            # Usamos get_object_or_404 para evitar caídas si se manipulan IDs en la URL
            origen_seleccionado = get_object_or_404(Lugar, id=origen_id)
            destino_seleccionado = get_object_or_404(Lugar, id=destino_id)

            todas_directas = list(Ruta.objects.filter(origen=origen_seleccionado, destino=destino_seleccionado))
            todos_transbordos = []
            
            rutas_desde_origen = Ruta.objects.filter(origen=origen_seleccionado)
            rutas_hacia_destino = Ruta.objects.filter(destino=destino_seleccionado)

            for t1 in rutas_desde_origen:
                for t2 in rutas_hacia_destino:
                    if t1.destino == t2.origen:
                        todos_transbordos.append({
                            'tramo1': t1, 'tramo2': t2, 'nodo_conexion': t1.destino,
                            'precio_total': t1.precio + t2.precio,
                            'tiempo_total': t1.tiempo_estimado_min + t2.tiempo_estimado_min,
                        })

            # Lógica de filtros
            if filtro_actual == 'todas':
                rutas_directas = todas_directas
                rutas_transbordo = todos_transbordos
            elif filtro_actual == 'direct':
                rutas_directas = todas_directas
                rutas_transbordo = []
            elif filtro_actual == 'cheapest':
                m_dir = min(todas_directas, key=lambda x: x.precio, default=None)
                m_tra = min(todos_transbordos, key=lambda x: x['precio_total'], default=None)
                if m_dir and m_tra:
                    if m_dir.precio <= m_tra['precio_total']:
                        rutas_directas, rutas_transbordo = [m_dir], []
                    else:
                        rutas_directas, rutas_transbordo = [], [m_tra]
                elif m_dir: rutas_directas = [m_dir]
                elif m_tra: rutas_transbordo = [m_tra]
            elif filtro_actual == 'fastest':
                m_dir = min(todas_directas, key=lambda x: x.tiempo_estimado_min, default=None)
                m_tra = min(todos_transbordos, key=lambda x: x['tiempo_total'], default=None)
                if m_dir and m_tra:
                    if m_dir.tiempo_estimado_min <= m_tra['tiempo_total']:
                        rutas_directas, rutas_transbordo = [m_dir], []
                    else:
                        rutas_directas, rutas_transbordo = [], [m_tra]
                elif m_dir: rutas_directas = [m_dir]
                elif m_tra: rutas_transbordo = [m_tra]

    total_rutas = len(rutas_directas) + len(rutas_transbordo)

    context = {
        'lugares': lugares,
        'rutas_directas': rutas_directas,
        'rutas_transbordo': rutas_transbordo,
        'origen_seleccionado': origen_seleccionado,
        'destino_seleccionado': destino_seleccionado,
        'busqueda_realizada': busqueda_realizada,
        'filtro_actual': filtro_actual,
        'total_rutas': total_rutas,
        'error_message': error_message, # Pasamos el error al template
    }
    return render(request, 'rutas/inicio.html', context)

# --- VISTA DETALLES con get_object_or_404 ---
def detalle_ruta(request, ruta_id):
    # ROBUSTEZ: Si la ruta no existe, muestra 404 en lugar de error 500
    ruta1 = get_object_or_404(Ruta, id=ruta_id)
    tramo2_id = request.GET.get('tramo2')
    
    es_transbordo = False
    ruta2 = None
    if tramo2_id:
        es_transbordo = True
        ruta2 = get_object_or_404(Ruta, id=tramo2_id)

    ahora = datetime.now()
    tiempo_solicitado = request.GET.get('time')

    if tiempo_solicitado:
        try:
            tiempo_obj = datetime.strptime(tiempo_solicitado, "%I:%M %p")
            hora_salida_obj = ahora.replace(hour=tiempo_obj.hour, minute=tiempo_obj.minute, second=0, microsecond=0)
        except ValueError:
            minutos_extra = 5 - (ahora.minute % 5) if (ahora.minute % 5) != 0 else 0
            hora_salida_obj = ahora + timedelta(minutes=minutos_extra)
    else:
        minutos_extra = 5 - (ahora.minute % 5) if (ahora.minute % 5) != 0 else 0
        hora_salida_obj = ahora + timedelta(minutes=minutos_extra)
        
    hora_salida = hora_salida_obj.strftime("%I:%M %p")
    
    if es_transbordo:
        tiempo_total = ruta1.tiempo_estimado_min + ruta2.tiempo_estimado_min
        precio_total = ruta1.precio + ruta2.precio
        nombre_ruta = "Mixed Route"
        origen_final = ruta1.origen
        destino_final = ruta2.destino
    else:
        tiempo_total = ruta1.tiempo_estimado_min
        precio_total = ruta1.precio
        nombre_ruta = ruta1.nombre
        origen_final = ruta1.origen
        destino_final = ruta1.destino

    hora_llegada_obj = hora_salida_obj + timedelta(minutes=tiempo_total)
    hora_llegada = hora_llegada_obj.strftime("%I:%M %p")

    paradas_con_tiempo = []
    alternativas_procesadas = []

    if es_transbordo:
        paradas_t1 = ruta1.get_paradas_list() if ruta1.get_paradas_list() else [f"Vía de {ruta1.nombre}"]
        paradas_t2 = ruta2.get_paradas_list() if ruta2.get_paradas_list() else [f"Vía de {ruta2.nombre}"]
        
        tiempo_por_tramo1 = ruta1.tiempo_estimado_min // (len(paradas_t1) + 1)
        tiempo_por_tramo2 = ruta2.tiempo_estimado_min // (len(paradas_t2) + 1)
        
        contador = 1
        tiempo_acumulado = hora_salida_obj
        
        paradas_con_tiempo.append({'numero': contador, 'nombre': origen_final.nombre, 'hora': hora_salida, 'tipo': 'origen', 'desc': f'Toma el bus: {ruta1.nombre}'})
        contador += 1
        for p in paradas_t1:
            tiempo_acumulado += timedelta(minutes=tiempo_por_tramo1)
            paradas_con_tiempo.append({'numero': contador, 'nombre': p, 'hora': tiempo_acumulado.strftime("%I:%M %p"), 'tipo': 'intermedia'})
            contador += 1
            
        tiempo_acumulado += timedelta(minutes=tiempo_por_tramo1)
        paradas_con_tiempo.append({'numero': contador, 'nombre': ruta1.destino.nombre, 'hora': tiempo_acumulado.strftime("%I:%M %p"), 'tipo': 'transbordo', 'desc': f'Cambia al bus: {ruta2.nombre}'})
        contador += 1
        for p in paradas_t2:
            tiempo_acumulado += timedelta(minutes=tiempo_por_tramo2)
            paradas_con_tiempo.append({'numero': contador, 'nombre': p, 'hora': tiempo_acumulado.strftime("%I:%M %p"), 'tipo': 'intermedia'})
            contador += 1
            
        paradas_con_tiempo.append({'numero': contador, 'nombre': destino_final.nombre, 'hora': hora_llegada, 'tipo': 'destino', 'desc': 'Llegada a destino final'})

        rutas_paralelas = Ruta.objects.filter(origen=origen_final, destino=destino_final).exclude(id=ruta_id)[:2]
        salida_prox = hora_salida_obj + timedelta(minutes=15)
        alternativas_procesadas.append({
            'ruta_id': ruta1.id, 'tramo2_id': ruta2.id, 'nombre_mostrar': "Mixed Route",
            'hora_salida': salida_prox.strftime("%I:%M %p"), 'hora_llegada': (salida_prox + timedelta(minutes=tiempo_total)).strftime("%I:%M %p"),
            'tipo_servicio': 'Mixed', 'precio': precio_total, 'tiempo': tiempo_total
        })
        for i, alt in enumerate(rutas_paralelas):
            salida_alt = hora_salida_obj + timedelta(minutes=20 * (i + 1))
            alternativas_procesadas.append({
                'ruta_id': alt.id, 'tramo2_id': None, 'nombre_mostrar': alt.nombre,
                'hora_salida': salida_alt.strftime("%I:%M %p"), 'hora_llegada': (salida_alt + timedelta(minutes=alt.tiempo_estimado_min)).strftime("%I:%M %p"),
                'tipo_servicio': 'Express' if alt.tiempo_estimado_min < 30 else 'Standard',
                'precio': alt.precio, 'tiempo': alt.tiempo_estimado_min
            })

    else:
        nombres_paradas = ruta1.get_paradas_list() if ruta1.get_paradas_list() else ["Ruta Habitual"]
        tiempo_por_tramo = tiempo_total // (len(nombres_paradas) + 1)
        
        paradas_con_tiempo.append({'numero': 1, 'nombre': origen_final.nombre, 'hora': hora_salida, 'tipo': 'origen', 'desc': 'Starting Point'})
        tiempo_acumulado = hora_salida_obj
        
        for i, nombre in enumerate(nombres_paradas):
            tiempo_acumulado += timedelta(minutes=tiempo_por_tramo)
            paradas_con_tiempo.append({'numero': i + 2, 'nombre': nombre, 'hora': tiempo_acumulado.strftime("%I:%M %p"), 'tipo': 'intermedia'})
            
        paradas_con_tiempo.append({'numero': len(nombres_paradas) + 2, 'nombre': destino_final.nombre, 'hora': hora_llegada, 'tipo': 'destino', 'desc': 'Destination'})

        rutas_paralelas = Ruta.objects.filter(origen=origen_final, destino=destino_final).exclude(id=ruta_id)[:2]
        salida_prox = hora_salida_obj + timedelta(minutes=15)
        alternativas_procesadas.append({
            'ruta_id': ruta1.id, 'tramo2_id': None, 'nombre_mostrar': ruta1.nombre,
            'hora_salida': salida_prox.strftime("%I:%M %p"), 'hora_llegada': (salida_prox + timedelta(minutes=tiempo_total)).strftime("%I:%M %p"),
            'tipo_servicio': 'Express' if tiempo_total < 30 else 'Standard', 'precio': precio_total, 'tiempo': tiempo_total
        })
        for i, alt in enumerate(rutas_paralelas):
            salida_alt = hora_salida_obj + timedelta(minutes=20 * (i + 1))
            alternativas_procesadas.append({
                'ruta_id': alt.id, 'tramo2_id': None, 'nombre_mostrar': alt.nombre,
                'hora_salida': salida_alt.strftime("%I:%M %p"), 'hora_llegada': (salida_alt + timedelta(minutes=alt.tiempo_estimado_min)).strftime("%I:%M %p"),
                'tipo_servicio': 'Express' if alt.tiempo_estimado_min < 30 else 'Standard',
                'precio': alt.precio, 'tiempo': alt.tiempo_estimado_min
            })

    context = {
        'ruta1_id': ruta1.id,
        'tramo2_id': tramo2_id,
        'nombre_ruta': nombre_ruta,
        'es_transbordo': es_transbordo,
        'origen_final': origen_final,
        'destino_final': destino_final,
        'tiempo_total': tiempo_total,
        'precio_total': precio_total,
        'hora_salida': hora_salida,
        'hora_llegada': hora_llegada,
        'paradas': paradas_con_tiempo,
        'alternativas': alternativas_procesadas,
    }
    
    return render(request, 'rutas/detalles.html', context)

# --- VISTA MAPA INTERACTIVO con get_object_or_404 ---
def mapa_ruta(request, ruta_id):
    ruta1 = get_object_or_404(Ruta, id=ruta_id)
    tramo2_id = request.GET.get('tramo2')
    
    es_transbordo = False
    ruta2 = None
    if tramo2_id:
        es_transbordo = True
        ruta2 = get_object_or_404(Ruta, id=tramo2_id)

    if es_transbordo:
        nombre_ruta = "Mixed Route"
        buses_list = [ruta1.nombre, ruta2.nombre]
        precio_total = ruta1.precio + ruta2.precio
        tiempo_total = ruta1.tiempo_estimado_min + ruta2.tiempo_estimado_min
        origen_final = ruta1.origen
        destino_final = ruta2.destino
    else:
        nombre_ruta = ruta1.nombre
        buses_list = [ruta1.nombre]
        precio_total = ruta1.precio
        tiempo_total = ruta1.tiempo_estimado_min
        origen_final = ruta1.origen
        destino_final = ruta1.destino

    buses_list = list(dict.fromkeys(buses_list))

    coord_origen = [origen_final.latitud, origen_final.longitud]
    coord_destino = [destino_final.latitud, destino_final.longitud]

    paradas_mapa = []
    calles_list = [] 
    
    def generar_paradas_mapa(ruta_obj, start_coord, end_coord, is_tramo2=False):
        p_nombres = ruta_obj.get_paradas_list() if ruta_obj.get_paradas_list() else [f"Vía de {ruta_obj.nombre}"]
        calles_list.extend(p_nombres)
        pasos = len(p_nombres) + 1
        lat_step = (end_coord[0] - start_coord[0]) / pasos
        lng_step = (end_coord[1] - start_coord[1]) / pasos
        
        nodos = []
        if not is_tramo2:
            nodos.append({
                "nombre": origen_final.nombre, "lat": start_coord[0], "lng": start_coord[1], 
                "tipo": "origen", "desc": f"Wait for bus {ruta1.nombre} heading to your destination."
            })
            
        for i, nombre in enumerate(p_nombres):
            nodos.append({
                "nombre": nombre, "lat": start_coord[0] + lat_step * (i+1), "lng": start_coord[1] + lng_step * (i+1), 
                "tipo": "intermedia", "desc": "The bus continues along its regular route."
            })
            
        if not es_transbordo or is_tramo2:
            nodos.append({
                "nombre": destino_final.nombre, "lat": end_coord[0], "lng": end_coord[1], 
                "tipo": "destino", "desc": "You have arrived at your destination."
            })
        else:
            nodos.append({
                "nombre": ruta1.destino.nombre, "lat": ruta1.destino.latitud, "lng": ruta1.destino.longitud, 
                "tipo": "transbordo", "desc": f"Get off and transfer to bus {ruta2.nombre}."
            })
            
        return nodos

    if es_transbordo:
        coord_transbordo = [ruta1.destino.latitud, ruta1.destino.longitud]
        paradas_mapa.extend(generar_paradas_mapa(ruta1, coord_origen, coord_transbordo))
        paradas_mapa.extend(generar_paradas_mapa(ruta2, coord_transbordo, coord_destino, is_tramo2=True))
    else:
        paradas_mapa = generar_paradas_mapa(ruta1, coord_origen, coord_destino)

    calles_list = list(dict.fromkeys(calles_list))

    context = {
        'nombre_ruta': nombre_ruta,
        'buses': buses_list,
        'calles': calles_list,
        'origen_nombre': origen_final.nombre,
        'destino_nombre': destino_final.nombre,
        'precio_total': precio_total,
        'tiempo_total': tiempo_total,
        'total_paradas': len(paradas_mapa),
        'paradas_json': json.dumps(paradas_mapa)
    }
    
    return render(request, 'rutas/mapa.html', context)

# Añade esto al final de views.py
def error_404(request, exception):
    return render(request, '404.html', status=404)