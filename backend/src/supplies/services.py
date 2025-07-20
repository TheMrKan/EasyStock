from datetime import date
from django.db.transaction import atomic
from rest_framework.exceptions import ValidationError

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

    def create(self):
        with atomic():
            supply = Supply(
                component=self.component,
                component_count=self.component_count,
                warehouse=self.warehouse,
                eta=self.eta,
            )
            supply.save()

            SupplyUpdater(supply).update_status(self.status)

        return supply


class SupplyUpdater:
    supply: Supply

    class InvalidSupplyStateError(DomainError):
        def __init__(self):
            self.code = "invalid_state"

    def __init__(self, supply: Supply):
        self.supply = supply

    @classmethod
    def validate_eta(cls, eta: date):
        if eta < date.today():
            raise ValidationError("Cant be in past", "cant_be_in_past")

    def update_status(self, new_status: Supply.Status):
        if new_status == self.supply.status:
            return

        if self.supply.status in (Supply.Status.RECEIVED, Supply.Status.CANCELLED):
            raise self.InvalidSupplyStateError()

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
