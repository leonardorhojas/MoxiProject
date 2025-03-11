from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.contenttypes.models import ContentType
from api.models import Medspa, Service, Appointment
from api.serializers import MedspaSerializer, ServiceSerializer, AppointmentSerializer

class MedspaViewSet(viewsets.ModelViewSet):
    queryset = Medspa.objects.all()
    serializer_class = MedspaSerializer

    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        medspa = self.get_object()
        services = Service.objects.filter(content_type=ContentType.objects.get_for_model(Medspa), object_id=medspa.id)
        return Response(ServiceSerializer(services, many=True).data)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if data.get('price_varies', False):
            data['price'] = None

        medspa = Medspa.objects.get(id=data['medspa_id'])
        data['content_type'] = ContentType.objects.get_for_model(Medspa).id
        data['object_id'] = medspa.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        services = Service.objects.filter(id__in=data['service_ids'])
        total_duration = sum(service.duration for service in services)
        total_price = sum(service.price or 0 for service in services)  # Handle None prices
        data['total_duration'] = total_duration
        data['total_price'] = total_price
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        appointment = serializer.instance
        appointment.services.set(services)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def filter_by_status(self, request):
        status_param = request.query_params.get('status', None)
        if status_param:
            appointments = Appointment.objects.filter(status=status_param)
            return Response(AppointmentSerializer(appointments, many=True).data)
        return Response({"error": "Status parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def filter_by_date(self, request):
        date_param = request.query_params.get('start_date', None)
        if date_param:
            appointments = Appointment.objects.filter(start_time__date=date_param)
            return Response(AppointmentSerializer(appointments, many=True).data)
        return Response({"error": "Start date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
