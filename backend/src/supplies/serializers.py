from rest_framework.serializers import ModelSerializer

from .models import Supply
from .services import SupplyUpdater


class SupplySerializer(ModelSerializer):

    def validate_eta(self, value):
        SupplyUpdater.validate_eta(value)
        return value

    class Meta:
        model = Supply
        fields = "__all__"
        read_only_fields = ("created", )

