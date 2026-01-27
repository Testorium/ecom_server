from typing import Annotated

from fastapi import Depends
from src.database.deps import DatabasePoolDep

from .repo import ProductRepository
from .service import ProductService


def get_product_service(db_pool: DatabasePoolDep) -> ProductService:
    repo = ProductRepository(db_pool)
    return ProductService(repo)


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
