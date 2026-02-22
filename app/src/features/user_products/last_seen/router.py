from fastapi import APIRouter
from src.routers.config import api_prefix_config


from .deps import LastSeenProductServiceDep


router = APIRouter(
    prefix=api_prefix_config.v1.last_seen_products, tags=["Last Seen Products"]
)


@router.get("/")
async def get_all_last_seen_products(
    last_seen_products_service: LastSeenProductServiceDep,
):
    return await last_seen_products_service.get_all()
