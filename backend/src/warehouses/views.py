from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from utils.exceptions import APIException
from .models import Warehouse, StockTransaction
from .serializers import (WarehouseSerializer, StockItemSerializer, StockTransactionSerializer,
                          TransactionCreateResponseSerializer)
from .services import WarehouseStockViewer, WarehouseTransactionManager


class WarehouseViewset(ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

    @action(detail=True, methods=["get"])
    def components(self, request, pk=None):
        warehouse: Warehouse = self.get_object()

        items = WarehouseStockViewer(warehouse).list_components()
        serializer = StockItemSerializer(items, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def products(self, request, pk=None):
        warehouse: Warehouse = self.get_object()

        items = WarehouseStockViewer(warehouse).list_products()
        serializer = StockItemSerializer(items, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def transactions(self, request, pk=None):
        warehouse = self.get_object()

        serializer = StockTransactionSerializer(warehouse.transactions, many=True)
        return Response(serializer.data)

    @transactions.mapping.post
    def transaction_create(self, request, pk=None):
        warehouse = self.get_object()

        serializer = StockTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            transaction = WarehouseTransactionManager(warehouse).make_transaction(
                StockTransaction.TransactionType.MANUAL,
                serializer.validated_data["item"],
                serializer.validated_data["quantity_delta"],
                extra=serializer.validated_data.get("extra", None)
            )

            stock = WarehouseStockViewer(warehouse).get_stock(serializer.validated_data["item"])
            response_serializer = TransactionCreateResponseSerializer({"transaction": transaction,
                                                                       "stock": stock})

            return Response(response_serializer.data, status.HTTP_201_CREATED)

        except WarehouseTransactionManager.ImpossibleTransactionError as e:
            raise APIException(status.HTTP_409_CONFLICT, str(e), code="insufficient_stock")

