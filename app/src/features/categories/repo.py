from typing import List, Optional

from asyncpg import Pool

from .schemas import Category, CategoryCreate, CategoryUpdate


class CategoryRepository:
    """category_tab"""

    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def create(
        self,
        data: CategoryCreate,
    ) -> Category:
        query = """
            INSERT INTO category_tab (name, description, parent_id)
            VALUES ($1, $2, $3)
            RETURNING category_id, name, description, parent_id
        """

        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                data.name,
                data.description,
                data.parent_id,
            )
        return Category(**dict(row))

    async def get_all(self) -> List[Category]:
        query = "SELECT category_id, name, description, parent_id FROM category_tab"
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(query)

        return [Category(**dict(row)) for row in rows]

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        query = """
        SELECT category_id, name, description, parent_id
        FROM category_tab WHERE category_id = $1
        ORDER BY category_id
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(query, category_id)

        return Category(**dict(row)) if row else None

    async def update_one_by_id(
        self,
        category_id: int,
        data: CategoryUpdate,
    ) -> Optional[Category]:
        query = """
        UPDATE category_tab
        SET name = COALESCE($1, name),
            description = COALESCE($2, description),
            parent_id = COALESCE($3, parent_id)
        WHERE category_id = $4
        RETURNING category_id, name, description, parent_id
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                data.name,
                data.description,
                data.parent_id,
                category_id,
            )
        return Category(**dict(row)) if row else None
