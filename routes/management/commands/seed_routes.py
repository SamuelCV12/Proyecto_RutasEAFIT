"""
Management command to seed the database with real EAFIT area routes.
Run: python manage.py seed_routes
"""
from django.core.management.base import BaseCommand
from routes.models import Route, Stop, StepInstruction


class Command(BaseCommand):
    help = 'Seed database with EAFIT transport routes'

    def handle(self, *args, **options):
        self.stdout.write('Seeding routes...')

        StepInstruction.objects.all().delete()
        Stop.objects.all().delete()
        Route.objects.all().delete()

        # ─── Ruta Buenos Aires: EAFIT → Barrio Buenos Aires ──────────────────
        r_ba = Route.objects.create(
            route_number='132',
            name='Buenos Aires',
            route_type='regular',
            origin='EAFIT University',
            destination='Barrio Buenos Aires',
            total_duration_minutes=25,
            fare_cop=3800,
            frequency_minutes=15,
        )

        stops_ba = [
            (1, 'EAFIT Universidad',       False,  0, 'Entrada principal Cra 49 con Cll 7 Sur',   6.200540, -75.577050),
            (2, 'Av. El Poblado / Cll 10', False,  6, 'Semáforo frente al Éxito El Poblado',      6.205000, -75.572000),
            (3, 'Cll 33 — Milla de Oro',   False, 12, 'Torre Coltejer, edificios bancarios',       6.220000, -75.571000),
            (4, 'Av. Greiff / Cll 44',     False, 18, 'Cerca al parque de Buenos Aires',           6.234000, -75.568000),
            (5, 'Barrio Buenos Aires',     False, 25, 'Parque principal del barrio Buenos Aires',  6.245000, -75.564000),
        ]

        stop_objs_ba = []
        for order, name, transfer, offset, landmark, lat, lng in stops_ba:
            s = Stop.objects.create(
                route=r_ba, order=order, name=name,
                is_transfer_point=transfer,
                arrival_offset_minutes=offset,
                landmark=landmark,
                latitude=lat, longitude=lng,
            )
            stop_objs_ba.append(s)

        steps_ba = [
            (1, 'walk',
             'Walk to the bus stop',
             'Camina hasta la parada',
             'Exit EAFIT through the main gate on Carrera 49. Turn right and walk 30 meters along the sidewalk. Look for people waiting at the roadside — there is no formal shelter, just a spot on the curb where the bus stops.',
             'Sal de EAFIT por la puerta principal de la Carrera 49. Gira a la derecha y camina 30 metros por el anden. Busca personas esperando al borde de la via — no hay paradero formal, solo un punto en el sardinel donde para el bus.',
             'Tip: Ask the security guard at the gate: "Donde para el bus 132?"',
             'Consejo: Pregunta al vigilante de la puerta: "Donde para el bus 132?"',
             3, stop_objs_ba[0]),

            (2, 'wait',
             'Wait for bus 132 — Buenos Aires',
             'Espera el bus 132 — Buenos Aires',
             'Wait at the roadside. The bus is a small blue-and-white minibus (buseta) that shows "BUENOS AIRES" or "132" on the front windshield. It comes every 15 minutes. Wave your hand clearly to flag it down — the driver will stop for you.',
             'Espera al borde de la via. El bus es una buseta pequena azul y blanca que muestra "BUENOS AIRES" o "132" en el parabrisas. Pasa cada 15 minutos. Levanta la mano para senalarlo — el conductor se detiene.',
             'Tip: You MUST wave your hand, otherwise the bus will not stop.',
             'Consejo: DEBES levantar la mano, de lo contrario el bus no para.',
             8, stop_objs_ba[0]),

            (3, 'board',
             'Board and pay $3,800',
             'Sube y paga $3.800',
             'Board through the front door next to the driver. Hand the driver exactly COP $3,800 in cash — have it ready before you get on. The driver handles money while driving, so keep the bills in your hand. Take any available seat.',
             'Sube por la puerta delantera, al lado del conductor. Entregale exactamente $3.800 en efectivo — tenlos listos antes de subir. El conductor maneja el dinero mientras conduce. Sientate donde haya espacio.',
             'Tip: Have exact change. $3.800 in bills or coins. Drivers often cannot break large bills like $50.000.',
             'Consejo: Ten el cambio exacto. $3.800 en billetes o monedas. Los conductores a menudo no pueden cambiar billetes de $50.000.',
             2, stop_objs_ba[0]),

            (4, 'ride',
             'Ride toward Buenos Aires',
             'Viaja hacia Buenos Aires',
             'Stay seated while the bus travels up Avenida El Poblado. You will pass the Milla de Oro financial district — tall glass buildings on your right. After that, the bus turns left uphill into the Buenos Aires neighborhood.',
             'Quédate sentado mientras el bus sube por la Avenida El Poblado. Pasaras la Milla de Oro — edificios de vidrio altos a tu derecha. Luego el bus gira a la izquierda cuesta arriba hacia el barrio Buenos Aires.',
             'Landmark: When you see the tall glass towers of the Milla de Oro, your stop is about 8 minutes away.',
             'Referencia: Cuando veas las torres de vidrio de la Milla de Oro, tu parada esta a unos 8 minutos.',
             17, stop_objs_ba[3]),

            (5, 'exit',
             'Exit at Buenos Aires park',
             'Bajate en el parque de Buenos Aires',
             'Tell the driver "Buenos Aires, por favor" when you board. When you see the main neighborhood park on your right, shout "Gracias!" to signal your stop. Exit through the front or rear door.',
             'Dile al conductor "Buenos Aires, por favor" cuando subas. Cuando veas el parque principal del barrio a tu derecha, grita "Gracias!" para indicar tu parada. Bajate por la puerta delantera o trasera.',
             'Say out loud: "Gracias!" — this signals the driver you want to get off.',
             'Di en voz alta: "Gracias!" — esto le indica al conductor que quieres bajarte.',
             2, stop_objs_ba[4]),

            (6, 'arrive',
             'You have arrived at Buenos Aires!',
             'Llegaste a Buenos Aires!',
             'You are at the main park of Barrio Buenos Aires. Total trip: 25 minutes. The park is the central landmark of the neighborhood.',
             'Estas en el parque principal del Barrio Buenos Aires. Viaje total: 25 minutos. El parque es el punto central del barrio.',
             '', '', 0, stop_objs_ba[4]),
        ]

        for step_num, stype, title_en, title_es, desc_en, desc_es, tip_en, tip_es, dur, stop in steps_ba:
            StepInstruction.objects.create(
                route=r_ba, step_number=step_num, step_type=stype,
                title_en=title_en, title_es=title_es,
                description_en=desc_en, description_es=desc_es,
                tip_en=tip_en, tip_es=tip_es,
                duration_minutes=dur, stop=stop,
            )

        # ─── Ruta El Poblado: EAFIT → Parque El Poblado ───────────────────────
        r_po = Route.objects.create(
            route_number='P02',
            name='El Poblado',
            route_type='regular',
            origin='EAFIT University',
            destination='Parque El Poblado',
            total_duration_minutes=20,
            fare_cop=3800,
            frequency_minutes=10,
        )

        stops_po = [
            (1, 'EAFIT Universidad',        False,  0, 'Entrada principal Cra 49',                  6.200540, -75.577050),
            (2, 'Cll 10 / Av. El Poblado',  False,  5, 'Frente al centro comercial Oviedo',         6.206000, -75.571000),
            (3, 'Los Balsos / Cll 16',       False, 11, 'Barrio Los Balsos, junto a restaurantes',   6.213000, -75.569000),
            (4, 'La Aguacatala',             False, 15, 'Cerca al puente de la Aguacatala',          6.218000, -75.567000),
            (5, 'Parque El Poblado',         False, 20, 'Parque principal de El Poblado',            6.208080, -75.568020),
        ]

        stop_objs_po = []
        for order, name, transfer, offset, landmark, lat, lng in stops_po:
            s = Stop.objects.create(
                route=r_po, order=order, name=name,
                is_transfer_point=transfer,
                arrival_offset_minutes=offset,
                landmark=landmark,
                latitude=lat, longitude=lng,
            )
            stop_objs_po.append(s)

        steps_po = [
            (1, 'walk',
             'Walk to the stop on Carrera 49',
             'Camina a la parada en la Carrera 49',
             'Exit EAFIT through the main gate. The bus stop is right outside on Carrera 49 — stand on the right side of the road facing downhill (south). The bus comes from the north heading south toward El Poblado.',
             'Sal por la puerta principal de EAFIT. La parada esta justo afuera en la Carrera 49 — parate en el lado derecho de la via mirando hacia el sur (cuesta abajo). El bus viene del norte hacia El Poblado.',
             'Tip: Stand on the RIGHT side of Cra 49, facing downhill (south).',
             'Consejo: Parate en el lado DERECHO de la Cra 49, mirando cuesta abajo (sur).',
             3, stop_objs_po[0]),

            (2, 'wait',
             'Wait for bus P02 — El Poblado',
             'Espera el bus P02 — El Poblado',
             'The bus is a small white or yellow minibus (buseta) showing "EL POBLADO" or "PARQUE POBLADO" on the front. It runs every 10 minutes. Wave your hand clearly to flag it — do not assume it will stop on its own.',
             'Es una buseta pequena blanca o amarilla que muestra "EL POBLADO" o "PARQUE POBLADO" en la parte delantera. Pasa cada 10 minutos. Levanta bien la mano para pararlo — no asumas que se va a detener solo.',
             'Tip: This route is frequent — if one is full, the next comes in 10 minutes.',
             'Consejo: Esta ruta es frecuente — si uno esta lleno, el siguiente viene en 10 minutos.',
             6, stop_objs_po[0]),

            (3, 'board',
             'Board and pay $3,800',
             'Sube y paga $3.800',
             'Board at the front door beside the driver. Pay COP $3,800 cash — exact amount preferred. Hand the money directly to the driver before sitting down. The bus may already be moving slightly, so hold the rail as you pay.',
             'Sube por la puerta delantera al lado del conductor. Paga $3.800 en efectivo — preferiblmente el monto exacto. Entregale el dinero al conductor antes de sentarte. El bus puede estar moviendose, asi que agarrate del pasamano.',
             'Tip: Coins are welcome. $3.800 = $2.000 + $1.000 + $500 + $200 + $100.',
             'Consejo: Las monedas son bienvenidas. $3.800 = $2.000 + $1.000 + $500 + $200 + $100.',
             2, stop_objs_po[0]),

            (4, 'ride',
             'Ride down Avenida El Poblado',
             'Viaja por la Avenida El Poblado',
             'The bus travels south along Avenida El Poblado. You will pass Oviedo mall on your left, then the Los Balsos neighborhood. The ride is mostly downhill and fast — stay alert for your stop.',
             'El bus va hacia el sur por la Avenida El Poblado. Pasaras el centro comercial Oviedo a tu izquierda, luego el barrio Los Balsos. El trayecto es mayormente cuesta abajo y rapido — mantente atento a tu parada.',
             'Landmark: Oviedo mall on the left = you are halfway there.',
             'Referencia: Centro comercial Oviedo a la izquierda = vas a la mitad del camino.',
             13, stop_objs_po[3]),

            (5, 'exit',
             'Exit at Parque El Poblado',
             'Bajate en el Parque El Poblado',
             'Tell the driver "Parque El Poblado, por favor" when you board. When you see the large tree-filled park on your right with restaurants all around, shout "Gracias!" to signal your stop. Exit through the front door.',
             'Dile al conductor "Parque El Poblado, por favor" al subir. Cuando veas el parque grande con arboles a tu derecha y restaurantes alrededor, grita "Gracias!". Bajate por la puerta delantera.',
             'Landmark: The park has a large ceiba tree in the center — very easy to spot.',
             'Referencia: El parque tiene una ceiba grande en el centro — muy facil de reconocer.',
             2, stop_objs_po[4]),

            (6, 'arrive',
             'You have arrived at El Poblado!',
             'Llegaste a El Poblado!',
             'You are at Parque El Poblado, the heart of the neighborhood. Total trip: 20 minutes. The park is surrounded by restaurants, cafes, and shops. From here you can walk to most addresses in El Poblado.',
             'Estas en el Parque El Poblado, el corazon del barrio. Viaje total: 20 minutos. El parque esta rodeado de restaurantes, cafes y tiendas.',
             '', '', 0, stop_objs_po[4]),
        ]

        for step_num, stype, title_en, title_es, desc_en, desc_es, tip_en, tip_es, dur, stop in steps_po:
            StepInstruction.objects.create(
                route=r_po, step_number=step_num, step_type=stype,
                title_en=title_en, title_es=title_es,
                description_en=desc_en, description_es=desc_es,
                tip_en=tip_en, tip_es=tip_es,
                duration_minutes=dur, stop=stop,
            )

        self.stdout.write(self.style.SUCCESS('Rutas cargadas exitosamente!'))
        self.stdout.write(f'   Ruta 132 Buenos Aires: {r_ba.stops.count()} paradas, {r_ba.steps.count()} pasos')
        self.stdout.write(f'   Ruta P02 El Poblado:   {r_po.stops.count()} paradas, {r_po.steps.count()} pasos')
