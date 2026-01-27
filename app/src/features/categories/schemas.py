from typing import List, Optional

from src.schema import BaseSchema


class Category(BaseSchema):
    id: int
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryCreate(BaseSchema):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryTree(BaseSchema):
    id: int
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    children: List["CategoryTree"] = []
