from typing import Annotated

from fastapi import Depends
from src.database.deps import DatabasePoolDep

from .repo import LastSeenProductRepository
from .service import LastSeenProductService


def get_last_seen_product_service(db_pool: DatabasePoolDep) -> LastSeenProductService:
    repo = LastSeenProductRepository(db_pool)
    return LastSeenProductService(repo)


LastSeenProductServiceDep = Annotated[
    LastSeenProductService, Depends(get_last_seen_product_service)
]
