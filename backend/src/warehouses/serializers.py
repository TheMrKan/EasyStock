from django.forms import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import (ModelSerializer, Serializer, Field)
from rest_framework.exceptions import ParseError

from .models import Warehouse, StockItem, StockTransaction
from .services import WarehouseStockViewer
from components.models import Component
from products.models import Product


class WarehouseSerializer(ModelSerializer):

    class Meta:
        model = Warehouse
        fields = ["id", "name"]


class StockItemSerializer(ModelSerializer):

    class Meta:
        model = StockItem
        fields = ["item_id", "quantity"]
        read_only_fields = ["item_id", "quantity"]


class ItemTypeField(Field):
    """
    Преобразует сокращенные названия типов предмета (component, product)
    в корректные content_type из django.contrib.contenttypes
    """

    COMPONENT = "component"
    PRODUCT = "product"

    def to_representation(self, value):
        if value == WarehouseStockViewer.get_item_type(Component):
            return self.COMPONENT
        elif value == WarehouseStockViewer.get_item_type(Product):
            return self.PRODUCT

        raise ValueError(f"Unknown item type: {value}")

    def to_internal_value(self, data):
        match data:
            case self.COMPONENT:
                return WarehouseStockViewer.get_item_type(Component)
            case self.PRODUCT:
                return WarehouseStockViewer.get_item_type(Product)
            case _:
                raise ParseError(f"Unknown item type: {data}")


class StockTransactionSerializer(ModelSerializer):

    item_type = ItemTypeField()

    class Meta:
        model = StockTransaction
        fields = ["id", "type", "item_type", "item_id", "quantity_delta", "timestamp", "extra"]
        read_only_fields = ["type"]

    def validate(self, data) -> None:
        try:
            item = data["item_type"].get_object_for_this_type(pk=data["item_id"])
        except ObjectDoesNotExist:
            raise ValidationError("Item not found", "item_not_found")
        
        data["item"] = item
        return data


class TransactionCreateResponseSerializer(Serializer):
    transaction = StockTransactionSerializer()
    stock = StockItemSerializer()
