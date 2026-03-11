# populate_data.py
# Script para poblar la base de datos con datos de prueba
# Ejecutar con: python manage.py shell < populate_data.py

from rutas.models import Parada, RutaBus, HorarioParada
from datetime import time

print("Creando paradas...")

# Paradas EAFIT y alrededores
paradas = [
    Parada.objects.create(
        nombre="Universidad EAFIT",
        latitud=6.200663,
        longitud=-75.578876,
        barrio="El Poblado"
    ),
    Parada.objects.create(
        nombre="Plaza Mayor",
        latitud=6.244203,
        longitud=-75.573434,
        barrio="Centro"
    ),
    Parada.objects.create(
        nombre="Parque Lleras",
        latitud=6.208419,
        longitud=-75.568466,
        barrio="El Poblado"
    ),
    Parada.objects.create(
        nombre="San Diego Mall",
        latitud=6.230833,
        longitud=-75.590556,
        barrio="Robledo"
    ),
    Parada.objects.create(
        nombre="El Tesoro",
        latitud=6.196111,
        longitud=-75.562222,
        barrio="El Poblado"
    ),
    Parada.objects.create(
        nombre="Av Las Vegas",
        latitud=6.207,
        longitud=-75.572,
        barrio="El Poblado"
    ),
    Parada.objects.create(
        nombre="Centro Comercial",
        latitud=6.235,
        longitud=-75.580,
        barrio="Laureles"
    ),
]

print(f"✓ Creadas {len(paradas)} paradas")

print("\nCreando rutas de bus...")

# Rutas de bus
rutas = [
    RutaBus.objects.create(
        numero_ruta="135",
        nombre="Expreso Universidad - Centro",
        origen="EAFIT Universidad",
        destino="Plaza Mayor",
        tipo_servicio="expreso",
        tarifa=2950,
        tiempo_estimado_minutos=25,
        activa=True
    ),
    RutaBus.objects.create(
        numero_ruta="78B",
        nombre="Estándar Poblado",
        origen="Plaza Mayor",
        destino="Parque Lleras",
        tipo_servicio="estandar",
        tarifa=2650,
        tiempo_estimado_minutos=15,
        activa=True
    ),
    RutaBus.objects.create(
        numero_ruta="234",
        nombre="Local EAFIT - Tesoro",
        origen="EAFIT Universidad",
        destino="El Tesoro",
        tipo_servicio="estandar",
        tarifa=2400,
        tiempo_estimado_minutos=10,
        activa=True
    ),
    RutaBus.objects.create(
        numero_ruta="42A",
        nombre="Expreso San Diego",
        origen="EAFIT Universidad",
        destino="San Diego Mall",
        tipo_servicio="expreso",
        tarifa=2950,
        tiempo_estimado_minutos=28,
        activa=True
    ),
]

print(f"✓ Creadas {len(rutas)} rutas")

print("\nCreando horarios de paradas...")

# Horarios para Ruta 135 (EAFIT -> Plaza Mayor)
ruta_135 = rutas[0]
HorarioParada.objects.create(ruta=ruta_135, parada=paradas[0], hora_paso=time(8, 15), orden=1, dias_operacion="LUN-VIE")
HorarioParada.objects.create(ruta=ruta_135, parada=paradas[5], hora_paso=time(8, 25), orden=2, dias_operacion="LUN-VIE")
HorarioParada.objects.create(ruta=ruta_135, parada=paradas[1], hora_paso=time(8, 35), orden=3, dias_operacion="LUN-VIE")

# Horarios para Ruta 78B (Plaza Mayor -> Parque Lleras)
ruta_78b = rutas[1]
HorarioParada.objects.create(ruta=ruta_78b, parada=paradas[1], hora_paso=time(8, 38), orden=1, dias_operacion="LUN-VIE")
HorarioParada.objects.create(ruta=ruta_78b, parada=paradas[6], hora_paso=time(8, 43), orden=2, dias_operacion="LUN-VIE")
HorarioParada.objects.create(ruta=ruta_78b, parada=paradas[2], hora_paso=time(8, 47), orden=3, dias_operacion="LUN-VIE")

# Horarios para Ruta 234 (EAFIT -> El Tesoro) - Ruta directa
ruta_234 = rutas[2]
HorarioParada.objects.create(ruta=ruta_234, parada=paradas[0], hora_paso=time(9, 0), orden=1, dias_operacion="LUN-SAB")
HorarioParada.objects.create(ruta=ruta_234, parada=paradas[4], hora_paso=time(9, 10), orden=2, dias_operacion="LUN-SAB")

# Horarios para Ruta 42A (EAFIT -> San Diego)
ruta_42a = rutas[3]
HorarioParada.objects.create(ruta=ruta_42a, parada=paradas[0], hora_paso=time(8, 30), orden=1, dias_operacion="LUN-VIE")
HorarioParada.objects.create(ruta=ruta_42a, parada=paradas[3], hora_paso=time(8, 58), orden=2, dias_operacion="LUN-VIE")

print("✓ Horarios creados exitosamente")

print("\n" + "="*50)
print("DATOS DE PRUEBA CARGADOS CORRECTAMENTE")
print("="*50)
print("\nResumen:")
print(f"- Paradas: {Parada.objects.count()}")
print(f"- Rutas: {RutaBus.objects.count()}")
print(f"- Horarios: {HorarioParada.objects.count()}")
print("\n✓ Ahora puedes probar la búsqueda de rutas combinadas")