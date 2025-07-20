from parameterized import parameterized
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta

from components.models import Component
from warehouses.models import Warehouse
from warehouses.serializers import WarehouseStockViewer
from .models import Supply
from .services import SupplyCreator


class TestCreateSupply(APITestCase):
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


class TestUpdateSupply(APITestCase):
    def setUp(self):
        self.component = Component.objects.create(name="Test Component", description="Desc")
        self.warehouse = Warehouse.objects.create(name="Main Warehouse")

    def test_post_not_allowed(self):
        supply = SupplyCreator(self.component, 5, self.warehouse, date.today() + timedelta(days=1), Supply.Status.PENDING).create()

        data = {
            "component": self.component.id,
            "component_count": 6,
            "warehouse": self.warehouse.id,
            "eta": (date.today() + timedelta(days=2)).isoformat(),
            "status": "RECEIVED"
        }
        response = self.client.post(f"/supplies/{supply.id}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_many_fields(self):
        supply = SupplyCreator(self.component, 5, self.warehouse, date.today() + timedelta(days=1), Supply.Status.PENDING).create()

        response = self.client.patch(f"/supplies/{supply.id}/", {"eta": (date.today() + timedelta(days=2)).isoformat(), "status": "RECEIVED"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].code, "invalid_fields")

    def test_update_unknown_field(self):
        supply = SupplyCreator(self.component, 5, self.warehouse, date.today() + timedelta(days=1), Supply.Status.PENDING).create()

        response = self.client.patch(f"/supplies/{supply.id}/", {"unknown_field": 1}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"].code, "unknown_field")

    def test_receive_supply(self):
        supply = SupplyCreator(self.component, 5, self.warehouse, date.today() + timedelta(days=1), Supply.Status.PENDING).create()

        response = self.client.patch(f"/supplies/{supply.id}/", {"status": "RECEIVED"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data["status"], "RECEIVED")

        self.assertEqual(WarehouseStockViewer(self.warehouse).get_stock_quantity(self.component), 5)

    def test_already_received_supply(self):
        supply = SupplyCreator(self.component, 5, self.warehouse, date.today() + timedelta(days=1), Supply.Status.RECEIVED).create()

        response = self.client.patch(f"/supplies/{supply.id}/", {"status": "RECEIVED"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.data["status"].code, "invalid")

        self.assertEqual(WarehouseStockViewer(self.warehouse).get_stock_quantity(self.component), 5)

    def test_cancel_supply(self):
        supply = SupplyCreator(self.component, 5, self.warehouse, date.today() + timedelta(days=1), Supply.Status.PENDING).create()

        response = self.client.patch(f"/supplies/{supply.id}/", {"status": "CANCELED"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data["status"], "CANCELED")

        self.assertEqual(WarehouseStockViewer(self.warehouse).get_stock_quantity(self.component), 0)

    def test_cancel_received_supply(self):
        supply = SupplyCreator(self.component, 5, self.warehouse, date.today() + timedelta(days=1), Supply.Status.RECEIVED).create()

        response = self.client.patch(f"/supplies/{supply.id}/", {"status": "CANCELED"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.data["status"].code, "invalid")

        self.assertEqual(WarehouseStockViewer(self.warehouse).get_stock_quantity(self.component), 5)


