from rest_framework.exceptions import ValidationError, MethodNotAllowed, ErrorDetail
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from utils.exceptions import APIException, DomainError
from .serializers import SupplySerializer
from .models import Supply
from .services import SupplyCreator, SupplyUpdater


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

        serializer.instance = supply

    def update(self, request, *args, **kwargs):
        # POST обновляет всю модель целиком. Разрешено только обновление одного поля
        if not kwargs.pop('partial', False):
            raise MethodNotAllowed("POST")

        if len(request.data) != 1:
            raise APIException(status.HTTP_400_BAD_REQUEST, "Exactly one field can be updated at once", code="invalid_fields")

        supply = self.get_object()
        serializer = self.get_serializer(supply, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        key, value = list(request.data.items())[0]

        try:
            match key:
                case 'status':
                    SupplyUpdater(supply).update_status(serializer.validated_data['status'])
                case _:
                    raise APIException(status.HTTP_400_BAD_REQUEST, "Unknown field", "unknown_field")

        except SupplyUpdater.NotChangedError:
            return Response(serializer.data, status=status.HTTP_200_OK)

        except DomainError as e:
            raise ValidationError({key: [ErrorDetail(e.message, code=e.code)]})

        response_serializer = SupplySerializer(supply)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
