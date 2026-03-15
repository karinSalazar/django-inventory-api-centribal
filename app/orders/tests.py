from django.test import TestCase
from .domain.models import Order, OrderItem

class OrderDomainTest(TestCase):
    """
    Pruebas unitarias para la lógica de negocio del Dominio de Pedidos.
    Estas pruebas no requieren base de datos (Unit Tests puros).
    """

    def setUp(self):
        # Configuramos datos de prueba reutilizables
        self.item1 = OrderItem(
            article_id=1,
            reference="ART-001",
            quantity=2,
            price_at_purchase=100.0,
            tax_rate=21.0  # 21% de IVA
        )
        self.item2 = OrderItem(
            article_id=2,
            reference="ART-002",
            quantity=1,
            price_at_purchase=50.0,
            tax_rate=10.0  # 10% de impuesto
        )

    def test_order_item_totals(self):
        """Valida que un ítem individual calcule sus totales correctamente."""
        # Item 1: 100 * 2 = 200 sin impuestos. 200 * 1.21 = 242 con impuestos.
        self.assertEqual(self.item1.total_without_tax, 200.0)
        self.assertEqual(self.item1.total_with_tax, 242.0)

    def test_order_aggregate_totals(self):
        """Valida que el Pedido sume correctamente los totales de todos sus ítems."""
        order = Order(items=[self.item1, self.item2])        
        self.assertEqual(order.total_price_without_tax, 250.0)
        self.assertEqual(order.total_price_with_tax, 297.0)

    def test_empty_order_totals(self):
        """Valida que un pedido sin artículos devuelva total 0."""
        empty_order = Order(items=[])
        self.assertEqual(empty_order.total_price_without_tax, 0)
        self.assertEqual(empty_order.total_price_with_tax, 0)