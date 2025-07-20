from rest_framework.exceptions import ErrorDetail
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status

from utils.exceptions import APIException
from .serializers import SupplySerializer
from .models import Supply
from .services import SupplyCreator


class SupplyViewSet(ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer

    def perform_create(self, serializer):
        supply = SupplyCreator(
            serializer.validated_data['component'],
            serializer.validated_data['component_count'],
            serializer.validated_data['warehouse'],
            serializer.validated_data['eta'],
            serializer.validated_data['status'],
        ).create()

        response_serializer = SupplySerializer(supply)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


