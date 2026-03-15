from django.urls import path
from .views import ArticleListCreateAPIView, ArticleDetailAPIView

urlpatterns = [
    path('', ArticleListCreateAPIView.as_view(), name='article-list-create'),
    path('<int:pk>/', ArticleDetailAPIView.as_view(), name='article-detail'),
]