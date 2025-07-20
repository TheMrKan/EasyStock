from django.contrib import admin

from .models import Supply


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    pass
