from rest_framework.serializers import ModelSerializer

from .models import Warehouse


class WarehouseSerializer(ModelSerializer):

    class Meta:
        model = Warehouse
        fields = ["id", "name"]