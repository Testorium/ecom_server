# delete all by user id

from asyncpg import Pool, Record

from .schemas import LastSeenProduct


class LastSeenProductRepository:
    table_name: str = "last_seen_products"

    def __init__(self, db_pool: Pool) -> None:
        self.db_pool = db_pool

    @staticmethod
    def _row_to_schema(row: Record) -> LastSeenProduct:
        return LastSeenProduct(**dict(row))

    async def _upsert(self, user_id: int, product_id: int) -> None:
        query = f"""
        INSERT INTO {self.table_name} (user_id, product_id, last_seen_at)
        VALUES ($1, $2, CURRENT_TIMESTAMP)
        ON CONFLICT (user_id, product_id)
        DO UPDATE SET last_seen_at = EXCLUDED.last_seen_at
        """
        async with self.db_pool.acquire() as conn:
            await conn.execute(query, user_id, product_id)

    async def _fetch_oldest_ids(self, user_id: int, offset: int) -> list[int]:
        query = f"""
        SELECT id
        FROM {self.table_name}
        WHERE user_id = $1
        ORDER BY last_seen_at ASC
        OFFSET $2
        """
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(query, user_id, offset)
            return [r["id"] for r in rows]

    async def _delete_by_ids(self, ids: list[int]) -> None:
        if not ids:
            return

        query = f"DELETE FROM {self.table_name} WHERE id = ANY($1::int[])"
        async with self.db_pool.acquire() as conn:
            await conn.execute(query, ids)

    async def delete_one_by_id(self, last_seen_product_id: int) -> bool:
        query = f"DELETE FROM {self.table_name} WHERE id = $1 RETURNING id"
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(query, last_seen_product_id)

        return row is not None
