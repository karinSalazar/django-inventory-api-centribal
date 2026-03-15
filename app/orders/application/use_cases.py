from typing import List, Optional
from ..domain.models import Order, OrderItem

class OrderUseCases:
    """
    Casos de uso para la gestión de pedidos.
    Implementa la lógica de validación de artículos y persistencia.
    """
    def __init__(self, order_repository, article_repository):
        self.order_repo = order_repository
        self.article_repo = article_repository

    def create_order(self, items_data: List[dict]) -> Order:
        """
        Crea un pedido validando que cada artículo exista en el inventario.
        items_data debe ser una lista de dicts: [{'article_id': 1, 'quantity': 2}, ...]
        """
        order_items = []
        
        for item in items_data:
            article_id = item.get('article_id')
            quantity = item.get('quantity')

            # REQUISITO: Comprobar la existencia de los artículos
            article = self.article_repo.get_by_id(article_id)
            if not article:
                raise ValueError(f"El artículo con ID {article_id} no existe.")

            # Creamos el objeto de dominio OrderItem con los datos reales del artículo
            # Esto asegura que el precio y el impuesto sean los vigentes al crear el pedido
            order_item = OrderItem(
                article_id=article.id,
                reference=article.reference,
                quantity=quantity,
                price_at_purchase=article.price_without_tax,
                tax_rate=article.tax_rate
            )
            order_items.append(order_item)

        new_order = Order(items=order_items)
        return self.order_repo.save(new_order)

    def list_orders(self) -> List[Order]:
        """Obtiene todos los pedidos registrados."""
        return self.order_repo.get_all()

    def get_order(self, order_id: int) -> Optional[Order]:
        """Obtiene un pedido específico por su ID único."""
        return self.order_repo.get_by_id(order_id)

    def update_order_items(self, order_id: int, items_data: List[dict]) -> Optional[Order]:
        """
        Modificar la lista de artículos incluidos en el pedido.
        """
        # Verificamos que el pedido exista primero
        existing_order = self.order_repo.get_by_id(order_id)
        if not existing_order:
            return None

        # Validamos los nuevos artículos (misma lógica que en la creación)
        new_order_items = []
        for item in items_data:
            article = self.article_repo.get_by_id(item.get('article_id'))
            if not article:
                raise ValueError(f"Artículo ID {item.get('article_id')} no encontrado.")
            
            new_order_items.append(OrderItem(
                article_id=article.id,
                reference=article.reference,
                quantity=item.get('quantity'),
                price_at_purchase=article.price_without_tax,
                tax_rate=article.tax_rate
            ))

        return self.order_repo.update_items(order_id, new_order_items)