from datetime import datetime
from typing import Optional

from pydantic import Field, PositiveInt
from src.schema import BaseSchema


class Product(BaseSchema):
    """
    Represents the product table in the database.
    """

    product_id: int
    name: str
    description: Optional[str] = None
    summary: Optional[str] = None
    category_id: int
    is_archived: bool
    created_at: datetime


class ProductCreate(BaseSchema):
    """
    Represents the required fields to create a new product.
    """

    name: str = Field(max_length=255)
    description: Optional[str] = None
    summary: Optional[str] = Field(None, max_length=255)
    category_id: int


class ProductUpdate(BaseSchema):
    """
    Represents optional fields to update an existing product.
    Allows partial updates.
    """

    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    summary: Optional[str] = Field(None, max_length=255)


class ProductStockUpdate(BaseSchema):
    """
    Represents the stock update for a product's quantity.
    """

    quantity: PositiveInt
