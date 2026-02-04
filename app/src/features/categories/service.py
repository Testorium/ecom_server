from typing import List, Optional

from src.service.base import BaseService
from src.service.exceptions import (
    ErrorMessages,
    NotFoundError,
    handle_asyncpg_exceptions,
)

from .error_messages import CATEGORY_ERROR_MESSAGES
from .repo import CategoryRepository
from .schemas import Category, CategoryCreate, CategoryTree, CategoryUpdate


class CategoryService(BaseService):
    error_messages = CATEGORY_ERROR_MESSAGES

    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def create(
        self,
        data: CategoryCreate,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> Category:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )

        with handle_asyncpg_exceptions(error_messages=error_messages):
            return await self.repo.create(data=data)

    async def get_one_by_id(
        self,
        category_id: int,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> Category:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )
        with handle_asyncpg_exceptions(error_messages=error_messages):
            category = await self.repo.get_by_id(category_id=category_id)

            if not category:
                raise NotFoundError

            return category

    async def get_all(
        self,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> List[CategoryTree]:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )
        with handle_asyncpg_exceptions(error_messages=error_messages):
            categories = await self.repo.get_all()

        return self.build_category_tree(
            [category.model_dump() for category in categories]
        )

    async def update_one_by_id(
        self,
        category_id: int,
        data: CategoryUpdate,
        error_messages: Optional[ErrorMessages | None] = None,
    ) -> Category:
        error_messages = self._get_error_messages(
            error_messages=error_messages,
            default_messages=self.error_messages,
        )

        with handle_asyncpg_exceptions(error_messages=error_messages):
            return await self.repo.update_one_by_id(
                category_id=category_id,
                data=data,
            )

    @staticmethod
    def build_category_tree(items):
        item_map = {}
        roots = []

        for item in items:
            item_map[item["id"]] = {**item, "children": []}

        for item in items:
            if item["parent_id"] in (None, 0):
                roots.append(item_map[item["id"]])
            else:
                parent = item_map.get(item["parent_id"])
                if parent:
                    parent["children"].append(item_map[item["id"]])

        return roots
