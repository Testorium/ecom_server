from typing import Annotated

from fastapi import Depends
from src.database.deps import DatabasePoolDep

from .repo import CategoryRepository
from .service import CategoryService


def get_category_service(db_pool: DatabasePoolDep) -> CategoryService:
    repo = CategoryRepository(db_pool=db_pool)
    return CategoryService(repo=repo)


CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]
