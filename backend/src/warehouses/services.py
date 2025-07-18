from django.contrib.contenttypes.models import ContentType
from django.db.transaction import atomic
from django.db.models import QuerySet

from .models import StockItem, Warehouse, StockTransaction
from components.models import Component
from products.models import Product


class WarehouseStockViewer:

    warehouse: Warehouse

    def __init__(self, warehouse: Warehouse):
        self.warehouse = warehouse

    @staticmethod
    def get_item_type(model) -> str:
        return ContentType.objects.get_for_model(model)
    
    def get_stock(self, item: Component | Product) -> StockItem | None:
        return self.warehouse.stock.filter(item_id=item.id, item_type=self.get_item_type(type(item))).first()

    def list_components(self) -> QuerySet:
        return self.warehouse.stock.filter(item_type=self.get_item_type(Component))
    
    def list_products(self) -> QuerySet:
        return self.warehouse.stock.filter(item_type=self.get_item_type(Product))
    

class WarehouseTransactionManager:

    warehouse: Warehouse

    class ImpossibleTransactionError(Exception):
        pass

    def __init__(self, warehouse: Warehouse):
        self.warehouse = warehouse

    def make_transaction(self,
                         type: str,
                         item: Component | Product,
                         quantity_delta: int,
                         extra: dict | None = None):
        if quantity_delta == 0:
            raise ValueError("Quantity delta can't be 0")
        
        with atomic():
            transaction = StockTransaction()
            transaction.warehouse = self.warehouse
            transaction.type = type
            transaction.item = item
            transaction.quantity_delta = quantity_delta
            transaction.extra = extra or {}
            transaction.save()

            stock = WarehouseStockViewer(self.warehouse).get_stock(item)
            if not stock:
                stock = StockItem(warehouse=self.warehouse,
                                  item=item,
                                  quantity=0)
            stock.quantity += quantity_delta

            if stock.quantity < 0:
                raise self.ImpossibleTransactionError("Got negative item quantity after the transaction")
            
            stock.save()