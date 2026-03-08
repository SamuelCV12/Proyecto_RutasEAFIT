from django.shortcuts import render, get_object_or_404
from django.utils.translation import get_language
from .models import Route, StepInstruction, Stop
from datetime import datetime, timedelta


def route_list(request):
    """Landing page showing available routes from/to EAFIT"""
    routes = Route.objects.prefetch_related('stops').all()
    lang = request.GET.get('lang', request.session.get('lang', 'en'))
    request.session['lang'] = lang
    context = {
        'routes': routes,
        'lang': lang,
    }
    return render(request, 'routes/route_list.html', context)


def route_guide(request, route_id):
    """Step-by-step guide for a specific route"""
    route = get_object_or_404(Route, id=route_id)
    steps = StepInstruction.objects.filter(route=route).select_related('stop').order_by('step_number')
    stops = Stop.objects.filter(route=route).order_by('order')

    lang = request.GET.get('lang', request.session.get('lang', 'en'))
    request.session['lang'] = lang

    # Calculate departure time based on query param or default to now
    departure_str = request.GET.get('departure', None)
    if departure_str:
        try:
            departure_time = datetime.strptime(departure_str, '%H:%M')
        except ValueError:
            departure_time = datetime.now().replace(second=0, microsecond=0)
    else:
        departure_time = datetime.now().replace(second=0, microsecond=0)

    # Build stop schedule
    stop_schedule = []
    for stop in stops:
        arrival = departure_time + timedelta(minutes=stop.arrival_offset_minutes)
        stop_schedule.append({
            'stop': stop,
            'arrival_time': arrival.strftime('%I:%M %p'),
        })

    arrival_time = departure_time + timedelta(minutes=route.total_duration_minutes)

    context = {
        'route': route,
        'steps': steps,
        'stops': stops,
        'stop_schedule': stop_schedule,
        'lang': lang,
        'departure_time': departure_time.strftime('%I:%M %p'),
        'arrival_time': arrival_time.strftime('%I:%M %p'),
        'departure_time_raw': departure_time.strftime('%H:%M'),
    }
    return render(request, 'routes/route_guide.html', context)
