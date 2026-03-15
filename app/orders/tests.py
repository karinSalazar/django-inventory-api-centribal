from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .domain.models import Order, OrderItem

class OrderTests(APITestCase):
    """
    Pruebas combinadas: Lógica de Dominio y Endpoints de API.
    """

    def setUp(self):
        # Datos para tests de Dominio
        self.item1 = OrderItem(
            article_id=1, reference="ART-001", quantity=2,
            price_at_purchase=100.0, tax_rate=21.0
        )
        self.item2 = OrderItem(
            article_id=2, reference="ART-002", quantity=1,
            price_at_purchase=50.0, tax_rate=10.0
        )

    # --- TESTS DE DOMINIO (Lógica pura) ---
    
    def test_order_item_totals(self):
        self.assertEqual(self.item1.total_without_tax, 200.0)
        self.assertEqual(self.item1.total_with_tax, 242.0)

    def test_order_aggregate_totals(self):
        order = Order(items=[self.item1, self.item2])        
        self.assertEqual(order.total_price_without_tax, 250.0)
        self.assertEqual(order.total_price_with_tax, 297.0)

    # --- TESTS DE API (Validación crítica) ---

    def test_create_order_with_non_existent_article_fails(self):
        """
        Punto crítico: Valida que si el artículo 999 no existe en DB, 
        la API responda con error 400.
        """
        url = '/api/orders/'  
        data = [{"article_id": 999, "quantity": 1}]
        
        response = self.client.post(url, data, format='json')
        
        # Verificamos que el código sea 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verificamos que el mensaje de error mencione que no existe
        self.assertIn("no existe", str(response.data).lower())