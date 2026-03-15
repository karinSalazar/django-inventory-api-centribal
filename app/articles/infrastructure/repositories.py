from typing import List, Optional
from .models import ArticleORM
from ..domain.models import Article

class DjangoArticleRepository:
    def _to_domain(self, orm_item: ArticleORM) -> Article:
        return Article(
            id=orm_item.id,
            reference=orm_item.reference,
            name=orm_item.name,
            description=orm_item.description,
            price_without_tax=float(orm_item.price_without_tax),
            tax_rate=float(orm_item.tax_rate),
            created_at=orm_item.created_at
        )
    
    def save(self, article: Article) -> Article:
        orm_article = ArticleORM.objects.create(
            reference=article.reference,
            name=article.name,
            description=article.description,
            price_without_tax=article.price_without_tax,
            tax_rate=article.tax_rate
        )
        return self._to_domain(orm_article) 
    
    def get_all(self) -> List[Article]:
        return [self._to_domain(item) for item in ArticleORM.objects.all()]

    def get_by_id(self, article_id: int) -> Optional[Article]:
        try:
            orm_item = ArticleORM.objects.get(id=article_id)
            return self._to_domain(orm_item)
        except ArticleORM.DoesNotExist:
            return None

    def update(self, article_id: int, data: dict) -> Optional[Article]:
        # Usamos filter().update() por eficiencia, pero verificamos existencia
        updated_rows = ArticleORM.objects.filter(id=article_id).update(**data)
        if updated_rows == 0:
            return None
        return self.get_by_id(article_id)