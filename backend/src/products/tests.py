from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import time

from .models import Product, ComponentRelation
from components.models import Component


class UpdateComponentRelationTestCase(APITestCase):

    url: str

    def setUp(self):
        Component.objects.create(name="Component 0", description="Description 0")
        Component.objects.create(name="Component 1", description="Description 1")

        Product.objects.create(name="Product 0", description="Description 0")

        self.url = reverse("product-update-component", args=["1"])

    def test_add(self):
        response = self.client.post(self.url, {"component": 1, "quantity": 3})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Product 0",
                "description": "Description 0",
                "components": [
                    {"component": 1, "quantity": 3},
                ],
            },
        )

        # если нужный объект не создался в БД, то .get() создаст исключение
        ComponentRelation.objects.filter(product__id=1, component__id=1, quantity=3).get()

        response = self.client.post(self.url, {"component": 2, "quantity": 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Product 0",
                "description": "Description 0",
                "components": [{"component": 1, "quantity": 3}, {"component": 2, "quantity": 5}],
            },
        )

        ComponentRelation.objects.filter(product__id=1, component__id=2, quantity=5).get()

    def test_add_not_exist(self):
        response = self.client.post(self.url, {"component": 4, "quantity": 3})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        response = self.client.post(self.url, {"component": 1, "quantity": 1})
        response = self.client.post(self.url, {"component": 2, "quantity": 6})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Product 0",
                "description": "Description 0",
                "components": [
                    {"component": 1, "quantity": 1},
                    {"component": 2, "quantity": 6},
                ],
            },
        )
        ComponentRelation.objects.filter(product__id=1, component__id=1, quantity=1).get()
        ComponentRelation.objects.filter(product__id=1, component__id=2, quantity=6).get()


class RemoveComponentRelationTestCase(APITestCase):
    url: str

    def setUp(self):
        c0 = Component.objects.create(name="Component 0", description="Description 0")
        c1 = Component.objects.create(name="Component 1", description="Description 1")
        Component.objects.create(name="Component 2", description="Description 2")

        p0 = Product.objects.create(name="Product 0", description="Description 0")

        ComponentRelation.objects.create(product=p0, component=c0, quantity=3)
        ComponentRelation.objects.create(product=p0, component=c1, quantity=5)

        self.url = reverse("product-update-component", args=["1"])

    def test_remove(self):
        response = self.client.post(self.url, {"component": 1, "quantity": 0})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Product 0",
                "description": "Description 0",
                "components": [
                    {"component": 2, "quantity": 5},
                ],
            },
        )

        response = self.client.post(self.url, {"component": 2, "quantity": 0})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Product 0",
                "description": "Description 0",
                "components": [],
            },
        )

    def test_remove_not_related(self):
        response = self.client.post(self.url, {"component": 3, "quantity": 0})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Product 0",
                "description": "Description 0",
                "components": [
                    {"component": 1, "quantity": 3},
                    {"component": 2, "quantity": 5},
                ],
            },
        )

    def test_remove_not_exist(self):
        response = self.client.post(self.url, {"component": 4, "quantity": 0})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
