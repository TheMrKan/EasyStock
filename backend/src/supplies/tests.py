from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta

from components.models import Component
from warehouses.models import Warehouse
from warehouses.serializers import WarehouseStockViewer
from supplies.models import Supply


class TestSupplyViewSet(APITestCase):
    def setUp(self):
        self.component = Component.objects.create(name="Test Component", description="Desc")
        self.warehouse = Warehouse.objects.create(name="Main Warehouse")

    def test_create_supply_success(self):
        data = {
            "component": self.component.id,
            "component_count": 50,
            "warehouse": self.warehouse.id,
            "eta": (date.today() + timedelta(days=1)).isoformat(),
            "status": "PENDING",
        }

        response = self.client.post("/supplies/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supply.objects.count(), 1)

        supply = Supply.objects.first()
        self.assertEqual(supply.status, Supply.Status.PENDING)
        self.assertEqual(supply.component, self.component)
        self.assertEqual(supply.warehouse, self.warehouse)
        self.assertEqual(supply.component_count, 50)

    def test_create_supply_with_invalid_eta(self):
        data = {
            "component": self.component.id,
            "component_count": 50,
            "warehouse": self.warehouse.id,
            "eta": (date.today() - timedelta(days=1)).isoformat(),
            "status": "PENDING",
        }

        response = self.client.post("/supplies/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Supply.objects.count(), 0)

        self.assertIn("eta", response.data)
        self.assertEqual("cant_be_in_past", response.data["eta"][0].code)

    def test_create_supply_received(self):
        data = {
            "component": self.component.id,
            "component_count": 50,
            "warehouse": self.warehouse.id,
            "eta": (date.today() + timedelta(days=1)).isoformat(),
            "status": "RECEIVED",
        }

        response = self.client.post("/supplies/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supply.objects.count(), 1)

        supply = Supply.objects.first()
        self.assertEqual(supply.status, Supply.Status.RECEIVED)
        self.assertEqual(supply.component, self.component)
        self.assertEqual(supply.warehouse, self.warehouse)
        self.assertEqual(supply.component_count, 50)

        self.assertEqual(WarehouseStockViewer(self.warehouse).get_stock(self.component).quantity, 50)

