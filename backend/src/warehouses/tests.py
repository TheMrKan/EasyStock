from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from components.models import Component
from products.models import Product
from .models import Warehouse


class StockTransactionTestCase(APITestCase):

    url: str
    comp1: Component
    prod1: Product
    warehouse1: Warehouse

    def setUp(self):
        self.comp1 = Component.objects.create(name="Component 1", description="Desc 1")
        self.prod1 = Product.objects.create(name="Product 1", description="Desc 1")
        self.warehouse1 = Warehouse.objects.create(name="Warehouse 1")

        self.url = reverse("warehouse-transactions", args=[self.warehouse1.id])

    def test_add_from_zero(self):
        response = self.client.post(self.url, {
            "warehouse": self.warehouse1.id,
            "item_type": "component",
            "item_id": 1,
            "quantity_delta": 2,
            "extra": {"comment": "Manual transaction"}
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        del data["transaction"]["timestamp"]

        self.assertEqual(
            data,
            {
                "transaction": {
                    "id": 1,
                    "warehouse": self.warehouse1.id,
                    "type": "manual",
                    "item_type": "component",
                    "item_id": 1,
                    "quantity_delta": 2,
                    "extra": {"comment": "Manual transaction"},
                },
                "stock": {
                    "item_id": 1,
                    "quantity": 2
                }
            },
        )

    def test_add_second_transaction(self):
        # Сначала создаем первую транзакцию
        self.client.post(self.url, {
            "warehouse": self.warehouse1.id,
            "item_type": "component",
            "item_id": 1,
            "quantity_delta": 2,
            "extra": {"comment": "First transaction"}
        }, format="json")

        # Добавляем вторую транзакцию
        response = self.client.post(self.url, {
            "warehouse": self.warehouse1.id,
            "item_type": "component",
            "item_id": 1,
            "quantity_delta": 3,
            "extra": {"comment": "Second transaction"}
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        del data["transaction"]["timestamp"]

        self.assertEqual(
            data,
            {
                "transaction": {
                    "id": 2,
                    "warehouse": self.warehouse1.id,
                    "type": "manual",
                    "item_type": "component",
                    "item_id": 1,
                    "quantity_delta": 3,
                    "extra": {"comment": "Second transaction"},
                },
                "stock": {
                    "item_id": 1,
                    "quantity": 5  # 2 + 3 = 5
                }
            },
        )

    def test_remove_item_from_stock(self):
        # Сначала добавляем 2 единицы
        self.client.post(self.url, {
            "warehouse": self.warehouse1.id,
            "item_type": "component",
            "item_id": self.comp1.id,
            "quantity_delta": 2,
            "extra": {"comment": "Initial stock"}
        }, format="json")

        # Теперь уменьшаем на 1
        response = self.client.post(self.url, {
            "warehouse": self.warehouse1.id,
            "item_type": "component",
            "item_id": self.comp1.id,
            "quantity_delta": -1,
            "extra": {"comment": "Removing one unit"}
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        del data["transaction"]["timestamp"]

        self.assertEqual(
            data,
            {
                "transaction": {
                    "id": 2,
                    "warehouse": self.warehouse1.id,
                    "type": "manual",
                    "item_type": "component",
                    "item_id": self.comp1.id,
                    "quantity_delta": -1,
                    "extra": {"comment": "Removing one unit"},
                },
                "stock": {
                    "item_id": self.comp1.id,
                    "quantity": 1  # 2 - 1 = 1
                }
            },
        )

    def test_cannot_remove_more_than_available(self):
        # Сначала добавляем 2 единицы
        self.client.post(self.url, {
            "warehouse": self.warehouse1.id,
            "item_type": "component",
            "item_id": self.comp1.id,
            "quantity_delta": 2,
            "extra": {"comment": "Initial stock"}
        }, format="json")

        # Пытаемся списать 3 единицы — больше, чем есть
        response = self.client.post(self.url, {
            "warehouse": self.warehouse1.id,
            "item_type": "component",
            "item_id": self.comp1.id,
            "quantity_delta": -3,
            "extra": {"comment": "Trying to remove more than available"}
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.json()["code"], "insufficient_stock")


class WarehouseTransactionHistoryTest(APITestCase):
    def setUp(self):
        self.warehouse = Warehouse.objects.create(name="Test Warehouse")
        self.product = Product.objects.create(name="Test Product")

    def test_transaction_history_for_product(self):
        url = reverse("warehouse-transactions", args=[self.warehouse.id])

        # Создаём несколько транзакций
        resp1 = self.client.post(url, {
            "warehouse": self.warehouse.id,
            "item_type": "product",
            "item_id": self.product.id,
            "quantity_delta": 15
        }, format="json")
        self.assertEqual(resp1.status_code, 201)

        resp2 = self.client.post(url, {
            "warehouse": self.warehouse.id,
            "item_type": "product",
            "item_id": self.product.id,
            "quantity_delta": -5
        }, format="json")
        self.assertEqual(resp2.status_code, 201)

        resp3 = self.client.post(url, {
            "warehouse": self.warehouse.id,
            "item_type": "product",
            "item_id": self.product.id,
            "quantity_delta": 3
        }, format="json")
        self.assertEqual(resp3.status_code, 201)

        # Получаем историю транзакций
        resp = self.client.get(url,)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)

        # Проверяем порядок (от новых к старым)
        self.assertEqual([tx["quantity_delta"] for tx in data], [3, -5, 15])

        # Проверяем структуру и значения
        for tx in data:
            self.assertEqual(tx["item_id"], self.product.id)
            self.assertEqual(tx["warehouse"], self.warehouse.id)
            self.assertIn("timestamp", tx)