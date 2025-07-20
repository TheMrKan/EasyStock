from rest_framework.routers import DefaultRouter

from .views import SupplyViewSet

router = DefaultRouter()

router.register("", SupplyViewSet)
