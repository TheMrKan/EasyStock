from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from components.models import Component
from products.models import Product


class Warehouse(models.Model):
    """
    Склад. На складах хранятся компоненты и продукты
    """

    id = models.BigAutoField(primary_key=True)
    name = models.CharField("Название", max_length=100)

    if TYPE_CHECKING:
        stock: "RelatedManager[StockItem]"

    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class StockItem(models.Model):
    """
    Отражает наличие предмета (компонента, продукта) на складе
    """

    pk = models.CompositePrimaryKey("warehouse_id", "item_type", "item_id")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Склад",
                                  related_name="stock")
    item_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Тип")
    item_id = models.BigIntegerField("Идентификатор")
    item = GenericForeignKey("item_type", "item_id")
    quantity = models.PositiveIntegerField("Количество")

    def __str__(self):
        return f"({self.warehouse.name}) {getattr(self.item, "name", self.item_id)} x {self.quantity}"

    class Meta:
        verbose_name = "Складской элемент"
        verbose_name_plural = "Складские элементы"
        indexes = [
            models.Index(fields=["warehouse_id"]),
            models.Index(fields=["warehouse_id", "item_type"]),
        ]


class StockTransaction(models.Model):
    """
    Лог добавления/удаления предметов со склада
    """

    class TransactionType(models.TextChoices):
        MANUAL = "manual"
        SUPPLY = "supply"

    id = models.BigAutoField(primary_key=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Склад",
                                  related_name="transactions")
    type = models.CharField("Тип транзакции", choices=TransactionType)
    item_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name="Тип предмета"
    )
    item_id = models.BigIntegerField("Идентификатор предмета")
    item = GenericForeignKey("item_type", "item_id")
    quantity_delta = models.IntegerField("Изменение количества")
    timestamp = models.DateTimeField("Время", auto_now_add=True)
    extra = models.JSONField("Дополнительные данные", default=dict)

    class Meta:
        verbose_name = "Складская транзакция"
        verbose_name_plural = "Складские транзакции"
        indexes = [
            models.Index(fields=["warehouse_id"]),
            models.Index(fields=["timestamp"])
        ]
