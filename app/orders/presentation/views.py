from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..application.use_cases import OrderUseCases
from ..infrastructure.repositories import DjangoOrderRepository
from app.articles.infrastructure.repositories import DjangoArticleRepository
from .serializers import OrderItemInputSerializer, OrderOutputSerializer

class OrderListCreateAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Usamos repositorios inyectados para cumplir con Arquitectura Hexagonal
        self.service = OrderUseCases(
            DjangoOrderRepository(), 
            DjangoArticleRepository()
        )

    def get(self, request):
        """Lista todos los pedidos con sus detalles."""
        orders = self.service.list_orders()
        serializer = OrderOutputSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Crea un pedido validando artículos y calculando totales."""
        serializer = OrderItemInputSerializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                # El caso de uso devuelve una entidad de Dominio
                order = self.service.create_order(serializer.validated_data)
                # Usamos el Serializer de salida para mostrar toda la info requerida
                return Response(OrderOutputSerializer(order).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = OrderUseCases(
            DjangoOrderRepository(), 
            DjangoArticleRepository()
        )

    def get(self, request, pk):
        """Obtiene un pedido específico."""
        order = self.service.get_order(pk)
        if not order:
            return Response({"error": "Pedido no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(OrderOutputSerializer(order).data)

    def put(self, request, pk):
        """
        Modificar la lista de artículos incluidos en el pedido.
        """
        serializer = OrderItemInputSerializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                order = self.service.update_order_items(pk, serializer.validated_data)
                if not order:
                    return Response({"error": "Pedido no encontrado"}, status=status.HTTP_404_NOT_FOUND)
                return Response(OrderOutputSerializer(order).data)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)