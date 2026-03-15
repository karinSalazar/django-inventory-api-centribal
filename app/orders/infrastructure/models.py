from django.db import models
from app.articles.infrastructure.models import ArticleORM

class OrderORM(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # Los campos de totales se calcularán en la lógica de negocio (Dominio)
    total_price_without_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_price_with_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'orders'

class OrderItemORM(models.Model):
    order = models.ForeignKey(OrderORM, related_name='items', on_delete=models.CASCADE)
    article = models.ForeignKey(ArticleORM, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    # Guardamos el precio del momento de la compra por histórico
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'