from typing import List

from fastapi import APIRouter
from src.routers.config import api_prefix_config

from .deps import CategoryServiceDep
from .schemas import Category, CategoryCreate, CategoryTree, CategoryUpdate

router = APIRouter(prefix=api_prefix_config.v1.categories, tags=["Category"])


@router.get("/", response_model=List[CategoryTree])
async def get_all_categories(
    category_service: CategoryServiceDep,
):
    return await category_service.get_all()


@router.post("/", response_model=Category)
async def create_new_category(
    data: CategoryCreate,
    category_service: CategoryServiceDep,
):
    return await category_service.create(data=data)


@router.get("/{category_id}")
async def get_one_category_by_id(
    category_id: int,
    category_service: CategoryServiceDep,
):
    return await category_service.get_one_by_id(category_id=category_id)


@router.patch("/{category_id}")
async def update_one_category_by_id(
    category_id: int,
    data: CategoryUpdate,
    category_service: CategoryServiceDep,
):
    return await category_service.update_one_by_id(
        category_id=category_id,
        data=data,
    )


# update_category_by_id
# delete_category_by_id
