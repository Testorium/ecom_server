from typing import Optional

from pydantic import Field, PositiveFloat, PositiveInt
from src.schema import BaseSchema


class Product(BaseSchema):
    """
    Represents the product table in the database.
    """

    id: int
    name: str
    price: float
    quantity: int
    description: Optional[str]


class ProductCreate(BaseSchema):
    """
    Represents the required fields to create a new product.
    """

    name: str
    price: PositiveFloat
    quantity: PositiveInt
    description: Optional[str] = Field(None, max_length=255)


class ProductUpdate(BaseSchema):
    """
    Represents optional fields to update an existing product.
    Allows partial updates.
    """

    name: Optional[str] = None
    price: Optional[PositiveFloat] = None
    quantity: Optional[PositiveInt] = None
    description: Optional[str] = Field(None, max_length=255)


class ProductStockUpdate(BaseSchema):
    """
    Represents the stock update for a product's quantity.
    """

    quantity: PositiveInt
