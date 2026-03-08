from django.db import models


class Route(models.Model):
    ROUTE_TYPE_CHOICES = [
        ('express', 'Express'),
        ('regular', 'Regular'),
        ('feeder', 'Feeder'),
    ]

    route_number = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    route_type = models.CharField(max_length=20, choices=ROUTE_TYPE_CHOICES, default='regular')
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    total_duration_minutes = models.IntegerField()
    fare_cop = models.DecimalField(max_digits=10, decimal_places=0)
    frequency_minutes = models.IntegerField(default=15, help_text="How often the bus comes (minutes)")

    def __str__(self):
        return f"Route {self.route_number} - {self.origin} → {self.destination}"

    class Meta:
        ordering = ['route_number']


class Stop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    order = models.IntegerField()
    name = models.CharField(max_length=100)
    is_transfer_point = models.BooleanField(default=False)
    arrival_offset_minutes = models.IntegerField(help_text="Minutes from departure of first stop")
    landmark = models.CharField(max_length=200, blank=True, help_text="Nearby landmark for reference")
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    def __str__(self):
        return f"{self.route.route_number} - Stop {self.order}: {self.name}"

    class Meta:
        ordering = ['route', 'order']


class StepInstruction(models.Model):
    STEP_TYPE_CHOICES = [
        ('walk', 'Walk'),
        ('wait', 'Wait'),
        ('board', 'Board Bus'),
        ('ride', 'Ride'),
        ('transfer', 'Transfer'),
        ('exit', 'Exit Bus'),
        ('arrive', 'Arrive'),
    ]

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='steps')
    step_number = models.IntegerField()
    step_type = models.CharField(max_length=20, choices=STEP_TYPE_CHOICES)
    title_en = models.CharField(max_length=200)
    title_es = models.CharField(max_length=200)
    description_en = models.TextField()
    description_es = models.TextField()
    tip_en = models.CharField(max_length=300, blank=True)
    tip_es = models.CharField(max_length=300, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    stop = models.ForeignKey(Stop, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Step {self.step_number}: {self.title_en}"

    class Meta:
        ordering = ['route', 'step_number']
