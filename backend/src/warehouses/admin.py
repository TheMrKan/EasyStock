from django.contrib import admin

from .models import Warehouse, StockItem, StockTransaction


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    pass
