from typing import List, Optional

from asyncpg import Pool, Record

from .schemas import Product, ProductCreate, ProductUpdate


class ProductRepository:
    """product_tab"""

    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    @staticmethod
    def _row_to_schema(row: Record) -> Product:
        return Product(**dict(row))

    async def create(self, data: ProductCreate) -> Product:
        query = """
        INSERT INTO product_tab (name, description, summary, category_id)
        VALUES ($1, $2, $3, $4)
        RETURNING product_id, name, description, summary, category_id,  is_archived, is_deleted, created_at
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                data.name,
                data.description,
                data.summary,
                data.category_id,
            )
        return self._row_to_schema(row)

    async def get_all(self) -> List[Product]:
        query = """
        SELECT product_id, name, description, summary, category_id, is_deleted, is_archived, created_at 
        FROM product_tab
        WHERE is_deleted = FALSE
        """
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(query)

        return [self._row_to_schema(row) for row in rows]

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        query = """
        SELECT product_id, name, description, summary, category_id, is_deleted, is_archived, created_at
        FROM product_tab WHERE product_id = $1
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(query, product_id)

        return self._row_to_schema(row) if row else None

    async def update_one_by_id(
        self,
        product_id: int,
        data: ProductUpdate,
    ) -> Optional[Product]:
        query = """
        UPDATE product_tab
        SET name = COALESCE($1, name),
            description = COALESCE($2, description),
            summary = COALESCE($3, summary)
        WHERE product_id = $4 AND is_deleted IS FALSE
        RETURNING product_id, name, description, summary, category_id, is_deleted, is_archived, created_at
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                data.name,
                data.description,
                data.summary,
                product_id,
            )
        return self._row_to_schema(row) if row else None

    async def delete_one_by_id(self, product_id: int) -> bool:
        query = "DELETE FROM product_tab WHERE product_id = $1 RETURNING product_id"
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(query, product_id)

        return row is not None

    async def soft_delete_one_by_id(self, product_id: int) -> bool:
        query = """UPDATE product_tab 
            SET is_deleted = $1 
            WHERE product_id = $2 
            RETURNING product_id"""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(query, True, product_id)

        return row is not None
