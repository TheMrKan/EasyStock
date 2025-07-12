from rest_framework.routers import DefaultRouter

from .views import WarehouseViewset

router = DefaultRouter()
router.register('', WarehouseViewset)