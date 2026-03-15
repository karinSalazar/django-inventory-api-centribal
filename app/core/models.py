from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class BaseEntity:
    """Clase base para todas las entidades de dominio."""
    id: Optional[int] = None
    created_at: Optional[datetime] = None