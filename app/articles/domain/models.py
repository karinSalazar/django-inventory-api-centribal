from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Article:
    reference: str
    name: str
    description: str
    price_without_tax: float
    tax_rate: float
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def calculate_price_with_tax(self) -> float:
        return self.price_without_tax * (1 + self.tax_rate / 100)