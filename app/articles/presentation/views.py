from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..application.use_cases import ArticleUseCases
from ..infrastructure.repositories import DjangoArticleRepository
from .serializers import ArticleSerializer    

class ArticleListCreateAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Inyectamos el repositorio en la clase de casos de uso
        self.service = ArticleUseCases(DjangoArticleRepository())

    def get(self, request):
        articles = self.service.get_all_articles()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            article = self.service.create_article(serializer.validated_data)
            return Response(ArticleSerializer(article).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetailAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ArticleUseCases(DjangoArticleRepository())

    def get(self, request, pk):
        article = self.service.get_article_by_id(pk)
        if not article:
            return Response({"error": "Artículo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(ArticleSerializer(article).data)

    def put(self, request, pk):
        serializer = ArticleSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            article = self.service.update_article(pk, serializer.validated_data)
            if not article:
                return Response({"error": "No se pudo actualizar"}, status=status.HTTP_404_NOT_FOUND)
            return Response(ArticleSerializer(article).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)