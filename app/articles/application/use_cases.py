from typing import List, Optional
from ..domain.models import Article

class ArticleUseCases:
    """
    Agrupa los casos de uso del módulo de artículos.
    """
    def __init__(self, repository):
        self.repository = repository

    def create_article(self, data: dict) -> Article:
        # En la lógica de creación aseguraremos que los tipos coincidan con la Entidad
        article = Article(
            reference=data.get('reference'),
            name=data.get('name'),
            description=data.get('description'),
            price_without_tax=data.get('price_without_tax'),
            tax_rate=data.get('tax_rate')
        )
        return self.repository.save(article)

    def get_all_articles(self) -> List[Article]:
        return self.repository.get_all()

    def get_article_by_id(self, article_id: int) -> Optional[Article]:
        return self.repository.get_by_id(article_id)

    def update_article(self, article_id: int, data: dict) -> Optional[Article]:
        return self.repository.update(article_id, data)