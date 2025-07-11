from components.serializers import ComponentSerializer
from rest_framework.serializers import (ModelSerializer, SerializerMethodField, 
                                        PrimaryKeyRelatedField, IntegerField)

from .models import Product, ComponentRelation
from components.models import Component


class ComponentRelationSerializer(ModelSerializer):
    component = PrimaryKeyRelatedField(queryset=Component.objects.all())
    quantity = IntegerField()

    class Meta:
        model = ComponentRelation
        fields = ["component", "quantity"]


class ProductSerializer(ModelSerializer):
    components = SerializerMethodField()

    def get_components(self, obj: Product):
        return ComponentRelationSerializer(obj.get_components(), many=True).data


    class Meta:
        model = Product
        fields = ["id", "name", "description", "components"]
        read_only_fields = ["components"]
