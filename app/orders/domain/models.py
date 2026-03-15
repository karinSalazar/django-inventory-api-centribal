from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class OrderItem:
    """
    Representa un artículo dentro de un pedido.
    Calcula los totales basándose en el precio base y el impuesto.
    """
    article_id: int
    reference: str
    quantity: int
    price_at_purchase: float  # Precio unitario sin impuestos
    tax_rate: float          # Ejemplo: 21.0 para 21%

    @property
    def total_without_tax(self) -> float:
        """Precio total de la línea sin impuestos."""
        return self.price_at_purchase * self.quantity

    @property
    def total_with_tax(self) -> float:
        """Precio total de la línea incluyendo el impuesto aplicable."""
        return self.total_without_tax * (1 + self.tax_rate / 100)


@dataclass
class Order:
    """
    Entidad de Dominio para el Pedido.
    Calcula los totales agregados de todos sus items.
    """
    items: List[OrderItem] = field(default_factory=list)
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    @property
    def total_price_without_tax(self) -> float:
        """Suma de los precios sin impuestos de todos los artículos."""
        return sum(item.total_without_tax for item in self.items)

    @property
    def total_price_with_tax(self) -> float:
        """Suma de los precios con impuestos de todos los artículos."""
        return sum(item.total_with_tax for item in self.items)