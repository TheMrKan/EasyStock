from datetime import date
from django.db.transaction import atomic
from rest_framework.exceptions import ValidationError, ErrorDetail

from utils.exceptions import DomainError
from .models import Supply
from components.models import Component
from warehouses.models import Warehouse, StockTransaction
from warehouses.services import WarehouseTransactionManager


class SupplyCreator:

    component: Component
    component_count: int
    warehouse: Warehouse
    eta: date
    status: Supply.Status

    def __init__(self,
                 component: Component,
                 component_count: int,
                 warehouse: Warehouse,
                 eta: date,
                 status: Supply.Status):
        self.component = component
        self.component_count = component_count
        self.warehouse = warehouse
        self.eta = eta
        self.status = status

    def create(self) -> Supply:
        with atomic():
            supply = Supply(
                component=self.component,
                component_count=self.component_count,
                warehouse=self.warehouse,
                eta=self.eta,
            )
            supply.save()

            try:
                SupplyUpdater(supply).update_status(self.status)
            except  SupplyUpdater.NotChangedError:
                pass

        return supply


class SupplyUpdater:
    supply: Supply

    class InvalidSupplyStatusError(DomainError):
        def __init__(self):
            super().__init__("Operation is not allowed with this status", "invalid_status")

    class NotChangedError(DomainError):
        def __init__(self):
            super().__init__("Supply status not changed", "not_changed")

    def __init__(self, supply: Supply):
        self.supply = supply

    @classmethod
    def validate_eta(cls, eta: date):
        if eta < date.today():
            # DRF-friendly: вложенный ValidationError для message+code
            raise ValidationError([ErrorDetail("ETA can't be in past", code="cant_be_in_past")])

    def assert_is_pending(self):
        if self.supply.status in (Supply.Status.RECEIVED, Supply.Status.CANCELED):
            raise self.InvalidSupplyStatusError()

    def update_status(self, new_status: Supply.Status):
        self.assert_is_pending()

        if new_status == self.supply.status:
            raise self.NotChangedError()

        with atomic():
            self.supply.status = new_status
            self.supply.save()

            if new_status == Supply.Status.RECEIVED:
                self.__receive()

    def __receive(self):
        extra = {
            "supply_id": self.supply.id
        }

        WarehouseTransactionManager(self.supply.warehouse).make_transaction(
            StockTransaction.TransactionType.SUPPLY,
            self.supply.component,
            self.supply.component_count,
            extra
        )
