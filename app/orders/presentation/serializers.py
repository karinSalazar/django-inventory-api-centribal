from rest_framework import serializers

class OrderItemInputSerializer(serializers.Serializer):
    """Para la creación y edición de items en el pedido."""
    article_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class OrderItemOutputSerializer(serializers.Serializer):
    """Requisito: Mostrar Referencia, Cantidad y Totales de cada artículo."""
    reference = serializers.CharField()
    quantity = serializers.IntegerField()
    total_without_tax = serializers.FloatField()
    total_with_tax = serializers.FloatField()

class OrderOutputSerializer(serializers.Serializer):
    """Serializador de salida basado en la Entidad de Dominio."""
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    items = OrderItemOutputSerializer(many=True)
    total_price_without_tax = serializers.FloatField()
    total_price_with_tax = serializers.FloatField()