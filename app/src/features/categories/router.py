from typing import List

from fastapi import APIRouter
from src.routers.config import api_prefix_config

from .deps import CategoryServiceDep
from .schemas import Category, CategoryCreate, CategoryTree, CategoryUpdate

router = APIRouter(prefix=api_prefix_config.v1.categories, tags=["Category"])


@router.get("/", response_model=List[CategoryTree])
async def get_all_categories(
    service: CategoryServiceDep,
):
    return await service.get_all()


@router.post("/", response_model=Category)
async def create_new_category(
    data: CategoryCreate,
    service: CategoryServiceDep,
):
    return await service.create(data=data)


@router.get("/{category_id}")
async def get_one_category_by_id(
    category_id: int,
    service: CategoryServiceDep,
):
    return await service.get_one_by_id(category_id=category_id)


@router.patch("/{category_id}")
async def update_one_category_by_id(
    category_id: int,
    data: CategoryUpdate,
    service: CategoryServiceDep,
):
    return await service.update_one_by_id(
        category_id=category_id,
        data=data,
    )


# update_category_by_id
# delete_category_by_id
