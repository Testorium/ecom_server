from typing import List, Optional

from asyncpg import Pool

from .schemas import Product, ProductCreate, ProductUpdate


class ProductRepository:
    table_name: str = "products"

    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def create(self, data: ProductCreate) -> Product:
        query = f"""
        INSERT INTO {self.table_name} (name, description, summary, category_id)
        VALUES ($1, $2, $3, $4)
        RETURNING id, name, description, summary, category_id, is_deleted, created_at
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                data.name,
                data.description,
                data.summary,
                data.category_id,
            )
        return Product(**dict(row))

    async def get_all(self) -> List[Product]:
        query = f"""SELECT id, name, description, summary, category_id, is_deleted, created_at 
        FROM {self.table_name}
        WHERE is_deleted = FALSE
        """
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(query)

        return [Product(**dict(row)) for row in rows]

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        query = f"""
        SELECT id, name, description, summary, category_id, is_deleted, created_at
        FROM {self.table_name} WHERE id = $1
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(query, product_id)

        return Product(**dict(row)) if row else None

    async def update_one_by_id(
        self,
        product_id: int,
        data: ProductUpdate,
    ) -> Optional[Product]:
        query = f"""
        UPDATE {self.table_name}
        SET name = COALESCE($1, name),
            description = COALESCE($2, description),
            summary = COALESCE($3, summary)
        WHERE id = $4 AND is_deleted IS FALSE
        RETURNING id, name, description, summary, category_id, is_deleted, created_at
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                data.name,
                data.description,
                data.summary,
                product_id,
            )
        return Product(**dict(row)) if row else None

    async def delete_one_by_id(self, product_id: int) -> bool:
        query = f"DELETE FROM {self.table_name} WHERE id = $1 RETURNING id"
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(query, product_id)

        return row is not None

    async def soft_delete_one_by_id(self, product_id: int) -> bool:
        query = f"""UPDATE {self.table_name} 
            SET is_deleted = $1 
            WHERE id = $2 
            RETURNING id"""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(query, True, product_id)

        return row is not None
