from django.db import models

from components.models import Component


class Product(models.Model):
    """
    Продукт, производимый компанией. Состоит из компонентов.
    """

    id = models.BigAutoField(primary_key=True)
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True, max_length=400)

    def get_components(self):
        return ComponentRelation.objects.filter(product=self).all()


    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        verbose_name = "Продукт (изделие)"
        verbose_name_plural = "Продукты (изделия)"


class ComponentRelation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    component = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name="Компонент")
    quantity = models.PositiveIntegerField("Количество")

    class Meta:
        unique_together = ('product', 'component')
