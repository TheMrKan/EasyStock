from django.urls import path, include
from rest_framework import routers

from .views import ComponentViewSet

router = routers.DefaultRouter()
router.register("", ComponentViewSet)
