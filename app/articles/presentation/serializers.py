from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    reference = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price_without_tax = serializers.FloatField()
    tax_rate = serializers.FloatField()
    created_at = serializers.DateTimeField(read_only=True)
