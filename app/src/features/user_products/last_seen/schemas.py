from datetime import datetime

from src.schema import BaseSchema
from src.features.products.schemas import Product


class LastSeenProduct(BaseSchema):
    id: int
    product: Product
    last_seen_at: datetime
