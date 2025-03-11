from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Medspa(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Supports "price varies"
    price_varies = models.BooleanField(default=False)  # Indicates if price is variable
    duration = models.PositiveIntegerField()  # Duration in minutes

    # Generic relationship for ownership
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    owner = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name


class Appointment(models.Model):
    start_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[("scheduled", "Scheduled"), ("completed", "Completed"), ("canceled", "Canceled")]
    )
    medspa = models.ForeignKey("Medspa", on_delete=models.CASCADE, related_name="appointments")
    services = models.ManyToManyField("Service", related_name="appointments")

    @property
    def total_duration(self):
        return sum(service.duration for service in self.services.all())

    @property
    def total_price(self):
        return sum(service.price or 0 for service in self.services.all())
