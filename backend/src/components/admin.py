from django.contrib import admin

from .models import Component

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    pass
