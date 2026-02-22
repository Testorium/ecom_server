from datetime import datetime

from src.features.categories.schemas import Category
from src.schema import BaseSchema
from src.features.products.schemas import Product


class LastSeenProduct(BaseSchema):
    last_seen_product_id: int
    last_seen_at: datetime
    product: Product
    category: Category
