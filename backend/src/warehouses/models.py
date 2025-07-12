from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from components.models import Component
from products.models import Product


class Warehouse(models.Model):
    """
    Склад. На складах хранятся компоненты и продукты
    """

    id = models.BigAutoField(primary_key=True)
    name = models.CharField("Название", max_length=100)

    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class StockItem(models.Model):
    """
    Отражает наличие предмета (компонента, продукта) на складе
    """

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

