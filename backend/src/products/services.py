from .models import Product, ComponentRelation
from components.models import Component


class ProductComponentsManager:
    """
    Управляет компонентами, из которых состоит продукт
    """

    product: Product

    def __init__(self, product: Product):
        self.product = product

    def __get_relation(self, component: Component) -> ComponentRelation:
        return ComponentRelation.objects.filter(product=self.product, component=component).first()

    def get_quantity(self, component: Component) -> int:
        relation = self.__get_relation(component)
        return relation.quantity if relation else 0

    def update_quantity(self, component: Component, quantity: int):
        if quantity < 0:
            raise ValueError("Quantity must be a non-negative number")

        if quantity == 0:
            self.__remove(component)
        elif self.get_quantity(component) == 0:
            self.__add(component, quantity)
        else:
            self.__update_quantity(component, quantity)

    def __add(self, component: Component, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be a positive number")

        relation = ComponentRelation(product=self.product,
                                     component=component,
                                     quantity=quantity)
        relation.save()

    def __update_quantity(self, component: Component, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be a positive number")
        
        relation = self.__get_relation(component)
        if not relation:
            raise RuntimeError(f"{component} hasn't been added to {self.product}")
        
        relation.quantity = quantity
        relation.save()

    def __remove(self, component: Component):
        relation = self.__get_relation(component)
        if relation:
            relation.delete()

