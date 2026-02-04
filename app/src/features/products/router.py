from typing import List

from fastapi import APIRouter, Path
from fastapi import status as status_code
from src.routers.config import api_prefix_config

from .deps import ProductServiceDep
from .schemas import (
    Product,
    ProductCreate,
    ProductUpdate,
)

router = APIRouter(prefix=api_prefix_config.v1.products, tags=["Products"])


@router.post("/", response_model=Product)
async def create_new_product(
    data: ProductCreate,
    service: ProductServiceDep,
) -> Product:
    return await service.create(data)


@router.get(
    "/",
    response_model=List[Product],
)
async def get_all_products(
    service: ProductServiceDep,
) -> List[Product]:
    return await service.get_all()


@router.get(
    "/{product_id}",
    response_model=Product,
)
async def get_one_product_by_id(
    service: ProductServiceDep,
    product_id: int = Path(..., ge=1),
) -> Product:
    return await service.get_one_by_id(product_id=product_id)


@router.delete("/{product_id}", status_code=status_code.HTTP_204_NO_CONTENT)
async def delete_one_product_by_id(
    service: ProductServiceDep,
    product_id: int = Path(..., ge=1),
) -> None:
    return await service.delete_one_by_id(product_id=product_id)


@router.delete("/{product_id}/soft", status_code=status_code.HTTP_204_NO_CONTENT)
async def soft_delete_one_product_by_id(
    service: ProductServiceDep,
    product_id: int = Path(..., ge=1),
) -> None:
    await service.soft_delete_one_by_id(product_id=product_id)


@router.patch("/{product_id}")
async def update_one_product_by_id(
    service: ProductServiceDep,
    data: ProductUpdate,
    product_id: int = Path(..., ge=1),
):
    await service.update_one_by_id(
        product_id=product_id,
        data=data,
    )
