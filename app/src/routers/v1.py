from fastapi import APIRouter
from src.features.categories.router import router as category_router
from src.features.products.router import router as product_router
from src.features.user_products.last_seen.router import (
    router as last_seen_router,
)

from .config import api_prefix_config

v1_router = APIRouter(prefix=api_prefix_config.v1.prefix)

v1_router.include_router(category_router)
v1_router.include_router(product_router)
v1_router.include_router(last_seen_router)
