from django.db import transaction
from typing import List, Optional
from .models import OrderORM, OrderItemORM
from ..domain.models import Order, OrderItem

class DjangoOrderRepository:
    """
    Implementación del repositorio de pedidos usando el ORM de Django.
    Se encarga de transformar datos de la DB a entidades de Dominio.
    """

    def _to_domain(self, orm_order: OrderORM) -> Order:
        """Helper para convertir de ORM a entidad de Dominio."""
        items = [
            OrderItem(
                article_id=item.article_id,
                reference=item.article.reference,
                quantity=item.quantity,
                price_at_purchase=float(item.price_at_purchase),
                tax_rate=float(item.article.tax_rate)
            ) for item in orm_order.items.all()
        ]
        return Order(
            id=orm_order.id,
            items=items,
            created_at=orm_order.created_at
        )

    def save(self, order: Order) -> Order:
        """Guarda un nuevo pedido y sus líneas de detalle."""
        with transaction.atomic():
            orm_order = OrderORM.objects.create(
                total_price_without_tax=order.total_price_without_tax,
                total_price_with_tax=order.total_price_with_tax
            )
            
            for item in order.items:
                OrderItemORM.objects.create(
                    order=orm_order,
                    article_id=item.article_id,
                    quantity=item.quantity,
                    price_at_purchase=item.price_at_purchase
                )
            
            return self._to_domain(orm_order)

    def get_all(self) -> List[Order]:
        """Lista todos los pedidos con sus artículos precargados."""
        qs = OrderORM.objects.prefetch_related('items__article').all()
        return [self._to_domain(orm_order) for orm_order in qs]

    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Obtiene un pedido por ID o devuelve None."""
        try:
            orm_order = OrderORM.objects.prefetch_related('items__article').get(id=order_id)
            return self._to_domain(orm_order)
        except OrderORM.DoesNotExist:
            return None

    def update_items(self, order_id: int, new_items: List[OrderItem]) -> Optional[Order]:
        """
        Modifica la lista de artículos.
        Elimina los items anteriores y crea los nuevos recalculando totales.
        """
        try:
            with transaction.atomic():
                orm_order = OrderORM.objects.get(id=order_id)
                
                # 1. Limpiamos items antiguos
                orm_order.items.all().delete()
                
                # 2. Creamos los nuevos items
                for item in new_items:
                    OrderItemORM.objects.create(
                        order=orm_order,
                        article_id=item.article_id,
                        quantity=item.quantity,
                        price_at_purchase=item.price_at_purchase
                    )
                
                # 3. Recalculamos totales en base a la lógica de dominio
                temp_order = Order(items=new_items)
                orm_order.total_price_without_tax = temp_order.total_price_without_tax
                orm_order.total_price_with_tax = temp_order.total_price_with_tax
                orm_order.save()
                
                return self._to_domain(orm_order)
        except OrderORM.DoesNotExist:
            return None