from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Component


class ComponentCreationTestCase(APITestCase):

    def test_create_empty_name(self):
        url = reverse('component-list')

        response = self.client.post(url, {"name": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["name"][0]["code"], "blank")

    def test_create_no_description(self):
        url = reverse("component-list")

        response = self.client.post(url, {"name": "Test component"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"id": 1, "name": "Test component", "description": ""})
        self.assertEqual(Component.objects.count(), 1)
        self.assertEqual(Component.objects.get().name, "Test component")
        self.assertEqual(Component.objects.get().description, "")

    def test_create(self):
        url = reverse("component-list")

        response = self.client.post(url, {"name": "Test component", "description": "Descr"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"id": 1, "name": "Test component", "description": "Descr"})
        self.assertEqual(Component.objects.count(), 1)
        self.assertEqual(Component.objects.get().name, "Test component")
        self.assertEqual(Component.objects.get().description, "Descr")


class ComponentUpdateTestCase(APITestCase):

    def setUp(self):
        Component.objects.create(name="Test", description="Descr")

    def test_update(self):
        url = reverse("component-detail", args=[1])

        response = self.client.put(url, {"name": "New name", "description": "New descr"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"id": 1, "name": "New name", "description": "New descr"})
        self.assertEqual(Component.objects.get().name, "New name")
        self.assertEqual(Component.objects.get().description, "New descr")

    def test_update_name_empty(self):
        url = reverse("component-detail", args=[1])

        response = self.client.put(url, {"name": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["name"][0]["code"], "blank")
        self.assertEqual(Component.objects.get().name, "Test")
