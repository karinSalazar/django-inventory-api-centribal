from django.urls import path
from .views import OrderListCreateAPIView, OrderDetailAPIView

urlpatterns = [
    # Ruta para listar y crear: /api/orders/
    path('', OrderListCreateAPIView.as_view(), name='order-list-create'),
    
    # Ruta para ver detalle y editar: /api/orders/<id>/
    path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
]