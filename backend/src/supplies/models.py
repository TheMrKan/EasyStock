from django.db import models

from components.models import Component
from warehouses.models import Warehouse


class Supply(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING'
        RECEIVED = 'RECEIVED'
        CANCELED = 'CANCELED'

    id = models.BigAutoField(primary_key=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name="Компонент")
    component_count = models.PositiveIntegerField(verbose_name="Количество")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Склад")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    eta = models.DateField(verbose_name="Дата прибытия")
    status = models.CharField(choices=Status.choices, default=Status.PENDING)

    class Meta:
        verbose_name = "Поставка"
        verbose_name_plural = "Поставки"


