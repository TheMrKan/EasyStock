from rest_framework.test import APITestCase
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
            "item_type": "component",
            "item_id": 1,
            "quantity_delta": 2,
            "extra": {"comment": "Manual transaction"}
        }, format="json")

        data = response.data
        del data["transaction"]["timestamp"]

        self.assertEqual(
            data,
            {
                "transaction": {
                    "id": 1,
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


