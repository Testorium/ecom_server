from typing import Any, List, Optional, Type, TypedDict

from asyncpg import Pool

from .schemas import Product, ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def create(self, product: ProductCreate) -> Product:
        query = """
        INSERT INTO products (name, price, quantity, description)
        VALUES ($1, $2, $3, $4)
        RETURNING id, name, price, quantity, description
        """
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                product.name,
                product.price,
                product.quantity,
                product.description,
            )
        return Product(**dict(row))

    # async def get_all(self) -> List[Product]:
    #     query = "SELECT id, name, price, quantity, description FROM products"
    #     async with self.db_pool.acquire() as conn:
    #         rows = await conn.fetch(query)
    #     return [Product(**dict(row)) for row in rows]

    # async def get_by_id(self, product_id: int) -> Optional[Product]:
    #     query = """
    #     SELECT id, name, price, quantity, description
    #     FROM products WHERE id = $1
    #     """
    #     async with self.db_pool.acquire() as conn:
    #         row = await conn.fetchrow(query, product_id)
    #     return Product(**dict(row)) if row else None

    # async def update(
    #     self, product_id: int, product: ProductUpdate
    # ) -> Optional[Product]:
    #     query = """
    #     UPDATE products
    #     SET name = COALESCE($1, name),
    #         price = COALESCE($2, price),
    #         quantity = COALESCE($3, quantity),
    #         description = COALESCE($4, description)
    #     WHERE id = $5
    #     RETURNING id, name, price, quantity, description
    #     """
    #     async with self.db_pool.acquire() as conn:
    #         row = await conn.fetchrow(
    #             query,
    #             product.name,
    #             product.price,
    #             product.quantity,
    #             product.description,
    #             product_id,
    #         )
    #     return Product(**dict(row)) if row else None

    # async def delete(self, product_id: int) -> bool:
    #     query = "DELETE FROM products WHERE id = $1 RETURNING id"
    #     async with self.db_pool.acquire() as conn:
    #         row = await conn.fetchrow(query, product_id)
    #     return row is not None
