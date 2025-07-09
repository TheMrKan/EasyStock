from django.db import models


class Component(models.Model):
    """
    Компонент. Из компонентов состоят продукты.
    """

    id = models.BigAutoField(primary_key=True)
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", max_length=400, blank=True)

    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        pass
