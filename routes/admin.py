from django.contrib import admin
from .models import Route, Stop, StepInstruction


class StopInline(admin.TabularInline):
    model = Stop
    extra = 1
    ordering = ['order']


class StepInstructionInline(admin.StackedInline):
    model = StepInstruction
    extra = 1
    ordering = ['step_number']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['route_number', 'name', 'route_type', 'origin', 'destination', 'total_duration_minutes', 'fare_cop']
    list_filter = ['route_type']
    search_fields = ['route_number', 'name', 'origin', 'destination']
    inlines = [StopInline, StepInstructionInline]


@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ['route', 'order', 'name', 'is_transfer_point', 'arrival_offset_minutes']
    list_filter = ['route', 'is_transfer_point']
    ordering = ['route', 'order']


@admin.register(StepInstruction)
class StepInstructionAdmin(admin.ModelAdmin):
    list_display = ['route', 'step_number', 'step_type', 'title_en']
    list_filter = ['route', 'step_type']
    ordering = ['route', 'step_number']
