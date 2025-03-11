import json

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from api.models import Medspa, Service, Appointment


class MedspaAPITestCase(APITestCase):
    def setUp(self):
        self.medspa = Medspa.objects.create(
            name="Luxury Medspa",
            address="123 Spa St",
            phone_number="1234567890",
            email="contact@luxuryspa.com"
        )
        self.content_type = ContentType.objects.get_for_model(Medspa)
        self.service = Service.objects.create(
            name="Botox",
            description="Wrinkle treatment",
            price=250.00,
            price_varies=False,
            duration=30,
            content_type=self.content_type,
            object_id=self.medspa.id
        )

    def test_create_medspa(self):
        data = {
            "name": "Elite Medspa",
            "address": "456 Elite St",
            "phone_number": "9876543210",
            "email": "elite@spa.com"
        }

        response = self.client.post(
            '/api/medspa/',
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_medspa_services(self):
        response = self.client.get(f'/api/medspa/{self.medspa.id}/services/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ServiceAPITestCase(APITestCase):
    def setUp(self):
        self.medspa = Medspa.objects.create(
            name="Luxury Medspa",
            address="123 Spa St",
            phone_number="1234567890",
            email="contact@luxuryspa.com"
        )

    def test_create_service_fixed_price(self):
        data = {
            "name": "Lip Flip",
            "description": "Enhances the upper lip",
            "price": 150.00,
            "price_varies": False,
            "duration": 30,
            "medspa_id": self.medspa.id
        }

        response = self.client.post(
            '/api/service/',
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['price'], "150.00")
        self.assertFalse(response.data['price_varies'])

    def test_create_service_variable_price(self):
        data = {
            "name": "Daxxify",
            "description": "Long-lasting neuromodulator",
            "price": None,
            "price_varies": True,
            "duration": 45,
            "medspa_id": self.medspa.id
        }

        response = self.client.post(
            '/api/service/',
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data['price'])
        self.assertTrue(response.data['price_varies'])


class AppointmentAPITestCase(APITestCase):
    def setUp(self):
        # Create Medspa
        self.medspa = Medspa.objects.create(
            name="Luxury Medspa",
            address="123 Spa St",
            phone_number="1234567890",
            email="contact@luxuryspa.com"
        )

        # Create Services
        self.service1 = Service.objects.create(
            name="Botox",
            description="Wrinkle treatment",
            price=250.00,
            price_varies=False,
            duration=30,
            content_type=ContentType.objects.get_for_model(Medspa),
            object_id=self.medspa.id
        )
        self.service2 = Service.objects.create(
            name="Daxxify",
            description="Long-lasting neuromodulator",
            price=300.00,
            price_varies=False,
            duration=45,
            content_type=ContentType.objects.get_for_model(Medspa),
            object_id=self.medspa.id
        )

        self.appointment = Appointment.objects.create(
            start_time="2025-03-11T14:00:00Z",
            status="scheduled",
            medspa=self.medspa
        )
        self.appointment.services.add(self.service1, self.service2)

    def test_create_appointment(self):
        """Test creating an appointment with multiple services"""
        data = {
            "start_time": "2025-03-12T10:00:00Z",
            "service_ids": [self.service1.id, self.service2.id],
            "medspa": self.medspa.id,
            "status": "scheduled"
        }

        response = self.client.post(
            "/api/appointment/",
            data=json.dumps(data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_duration'], 75)  # 30 + 45
        self.assertEqual(response.data['total_price'], 550.00)  # 250 + 300
        self.assertEqual(response.data['status'], "scheduled")

    def test_get_appointment_by_id(self):
        """Test retrieving a specific appointment"""
        response = self.client.get(f"/api/appointment/{self.appointment.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.appointment.id)
        self.assertEqual(response.data['status'], "scheduled")

    def test_update_appointment_status(self):
        """Test updating an appointment's status"""
        response = self.client.patch(
            f"/api/appointment/{self.appointment.id}/",
            data=json.dumps({"status": "completed"}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "completed")

    def test_list_appointments(self):
        """Test retrieving a list of all appointments"""
        response = self.client.get("/api/appointment/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)  # Ensure at least 1 appointment exists

    def test_filter_appointments_by_status(self):
        """Test filtering appointments by status"""
        response = self.client.get("/api/appointment/filter_by_status/?status=scheduled")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.data[0]['status'], "scheduled")

    def test_filter_appointments_by_date(self):
        """Test filtering appointments by start date"""
        response = self.client.get("/api/appointment/filter_by_date/?start_date=2025-03-11")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
