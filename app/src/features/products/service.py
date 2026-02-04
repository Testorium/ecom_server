from typing import List, Optional

from src.service.base import BaseService
from src.service.exceptions import (
    ErrorMessages,
    NotFoundError,
    handle_asyncpg_exceptions,
)

from .error_messages import PRODUCT_ERROR_MESSAGES
from .repo import ProductRepository
from .schemas import Product, ProductCreate, ProductUpdate


class ProductService(BaseService):
    error_messages = PRODUCT_ERROR_MESSAGES

    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def create(
        self,
        data: ProductCreate,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> Product:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )

        with handle_asyncpg_exceptions(error_messages=error_messages):
            return await self.repo.create(data)

    async def get_all(
        self,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> List[Product]:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )
        with handle_asyncpg_exceptions(error_messages=error_messages):
            return await self.repo.get_all()

    async def get_one_by_id(
        self,
        product_id: int,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> Product:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )
        with handle_asyncpg_exceptions(error_messages=error_messages):
            product = await self.repo.get_by_id(product_id=product_id)

            if not product:
                raise NotFoundError

            return product

    async def delete_one_by_id(
        self,
        product_id: int,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> None:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )

        with handle_asyncpg_exceptions(error_messages=error_messages):
            result = await self.repo.delete_one_by_id(product_id=product_id)

            if not result:
                raise NotFoundError

            return None

    async def soft_delete_one_by_id(
        self,
        product_id: int,
        error_messages: Optional[ErrorMessages | None] = None,
    ):
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )

        with handle_asyncpg_exceptions(error_messages=error_messages):
            result = await self.repo.soft_delete_one_by_id(product_id=product_id)

            if not result:
                raise NotFoundError

            return None

    async def update_one_by_id(
        self,
        product_id: int,
        data: ProductUpdate,
        error_messages: Optional[ErrorMessages | None] = None,
    ):
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )

        with handle_asyncpg_exceptions(error_messages=error_messages):
            result = await self.repo.update_one_by_id(
                product_id=product_id,
                data=data,
            )

            if not result:
                raise NotFoundError

            return result
