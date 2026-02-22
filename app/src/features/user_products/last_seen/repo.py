# delete all by user id
from typing import List
from asyncpg import Pool, Record


from src.features.products.schemas import Product
from src.features.categories.schemas import Category

from .schemas import LastSeenProduct


class LastSeenProductRepository:
    """last_seen_product_tab"""

    def __init__(self, db_pool: Pool) -> None:
        self.db_pool = db_pool

    @staticmethod
    def _row_to_schema(row: Record) -> LastSeenProduct:
        return LastSeenProduct(**dict(row))

    async def _upsert(self, user_id: int, product_id: int) -> None:
        query = """
        INSERT INTO last_seen_product_tab (user_id, product_id, last_seen_at)
        VALUES ($1, $2, CURRENT_TIMESTAMP)
        ON CONFLICT (user_id, product_id)
        DO UPDATE SET last_seen_at = EXCLUDED.last_seen_at
        """
        async with self.db_pool.acquire() as conn:
            await conn.execute(query, user_id, product_id)

    async def _fetch_oldest_ids(self, user_id: int, offset: int) -> List[int]:
        query = """
        SELECT last_seen_product_id
        FROM last_seen_product_tab
        WHERE user_id = $1
        ORDER BY last_seen_at ASC
        OFFSET $2
        """
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(query, user_id, offset)
            return [r["last_seen_product_id"] for r in rows]

    async def _delete_by_ids(self, ids: List[int]) -> None:
        if not ids:
            return

        query = "DELETE FROM last_seen_product_tab WHERE last_seen_product_id = ANY($1::int[])"
        async with self.db_pool.acquire() as conn:
            await conn.execute(query, ids)

    async def delete_one_by_id(self, last_seen_product_id: int) -> bool:
        query = "DELETE FROM last_seen_product_tab WHERE last_seen_product_id = $1 RETURNING last_seen_product_id"
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(query, last_seen_product_id)

        return row is not None

    async def get_all(self) -> Record:
        query = """
        SELECT 
            t.last_seen_product_id,
            t.last_seen_at,
            t1.product_id,
            t1.name AS product_name,
            t1.description,
            t1.summary AS product_summary,
            t1.created_at,
            t1.is_archived,
            t2.category_id,
            t2.name AS category_name
        FROM last_seen_product_tab t
        JOIN product_tab t1 ON t.product_id = t1.product_id
        JOIN category_tab t2 ON t1.category_id = t2.category_id
        WHERE t1.is_deleted = FALSE;
        """

        async with self.db_pool.acquire() as conn:
            row = await conn.fetch(query)

        print(row)
        product = Product(
            product_id=row["product_id"],
            name=row["product_name"],
            description=row["description"],
            summary=row["product_summary"],
            is_archived=row["is_archived"],
            is_deleted=False,
            created_at=row["created_at"],
        )

        category = Category(category_id=row["category_id"], name=row["category_name"])

        last_seen = LastSeenProduct(
            last_seen_product_id=row["last_seen_product_id"],
            last_seen_at=row["last_seen_at"],
            product=product,
            category=category,
        )

        return last_seen
