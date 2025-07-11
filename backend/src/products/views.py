from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from utils.exceptions import APIException

from .models import Product
from .serializers import ProductSerializer, ComponentRelationSerializer
from .services import ProductComponentsManager


class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=["post"])
    def update_component(self, request, pk: int):
        product = self.get_object()

        serializer = ComponentRelationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            ProductComponentsManager(product).update_quantity(serializer.validated_data["component"],
                                                             serializer.validated_data["quantity"])
            
            response_serializer = ProductSerializer(product)
            return Response(response_serializer.data)
        except ValueError:
            raise APIException("Invalid quantity", code=status.HTTP_400_BAD_REQUEST)


