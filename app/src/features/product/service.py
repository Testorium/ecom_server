from typing import Optional, cast

from src.service.exceptions import (
    DEFAULT_ERROR_MESSAGES,
    ErrorMessages,
    handle_asyncpg_exceptions,
)

from .error_messages import PRODUCT_ERROR_MESSAGES
from .repo import ProductRepository
from .schemas import Product, ProductCreate


class ProductService:
    error_messages: ErrorMessages = PRODUCT_ERROR_MESSAGES

    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def create(
        self,
        product: ProductCreate,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> Product:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )

        with handle_asyncpg_exceptions(error_messages=error_messages):
            return await self.repo.create(product)

    # async def list_products(self) -> List[Product]:
    #     return await self.repo.get_all()

    # async def get_product(self, product_id: int) -> Product:
    #     product = await self.repo.get_by_id(product_id)
    #     if not product:
    #         raise HTTPException(404, "Product not found")
    #     return product

    # async def update_product(self, product_id: int, product: ProductUpdate) -> Product:
    #     updated = await self.repo.update(product_id, product)
    #     if not updated:
    #         raise HTTPException(404, "Product not found")
    #     return updated

    # async def delete_product(self, product_id: int) -> None:
    #     deleted = await self.repo.delete(product_id)
    #     if not deleted:
    #         raise HTTPException(404, "Product not found")

    @staticmethod
    def _get_error_messages(
        error_messages: Optional[ErrorMessages | None] = None,
        default_messages: Optional[ErrorMessages | None] = None,
    ) -> ErrorMessages:
        messages = cast("ErrorMessages", dict(DEFAULT_ERROR_MESSAGES))

        if default_messages:
            messages.update(default_messages)

        if error_messages:
            messages.update(error_messages)

        return messages
