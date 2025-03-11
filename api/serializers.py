from rest_framework import serializers
from api.models import Medspa, Service, Appointment


class MedspaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medspa
        fields = ['id', 'name', 'address', 'phone_number', 'email']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'price_varies', 'duration', 'object_id', 'content_type']

    def validate(self, data):
        if data.get('price_varies', False) and data.get('price') is not None:
            raise serializers.ValidationError("If price_varies is True, price must be None.")
        return data


class AppointmentSerializer(serializers.ModelSerializer):
    service_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    total_duration = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ["id", "start_time", "status", "medspa", "service_ids", "total_duration", "total_price"]

    def create(self, validated_data):
        service_ids = validated_data.pop("service_ids")
        appointment = Appointment.objects.create(**validated_data)
        appointment.services.set(Service.objects.filter(id__in=service_ids))
        return appointment

    def get_total_duration(self, obj):
        return sum(service.duration for service in obj.services.all())

    def get_total_price(self, obj):
        return sum(service.price or 0 for service in obj.services.all())

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["services"] = [{"id": service.id, "name": service.name} for service in instance.services.all()]
        return representation