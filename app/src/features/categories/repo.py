from typing import List, Optional

from asyncpg import Pool

from .schemas import Category, CategoryCreate, CategoryUpdate


class CategoryRepository:
    table_name: str = "categories"

    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def create(
        self,
        data: CategoryCreate,
    ) -> Category:
        query = f"""
            INSERT INTO {self.table_name} (name, description, parent_id)
            VALUES ($1, $2, $3)
            RETURNING id, name, description, parent_id 
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
        query = f"SELECT id, name, description, parent_id FROM {self.table_name}"
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(query)

        return [Category(**dict(row)) for row in rows]

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        query = f"""
        SELECT id, name, description, parent_id
        FROM {self.table_name} WHERE id = $1
        ORDER BY id
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(query, category_id)

        return Category(**dict(row)) if row else None

    async def update_one_by_id(
        self,
        category_id: int,
        data: CategoryUpdate,
    ) -> Optional[Category]:
        query = f"""
        UPDATE {self.table_name}
        SET name = COALESCE($1, name),
            description = COALESCE($2, description),
            parent_id = COALESCE($3, parent_id)
        WHERE id = $4
        RETURNING id, name, description, parent_id
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

    # async def delete(self, product_id: int) -> bool:
    #     query = "DELETE FROM products WHERE id = $1 RETURNING id"
    #     async with self.db_pool.acquire() as conn:
    #         row = await conn.fetchrow(query, product_id)
    #     return row is not None
