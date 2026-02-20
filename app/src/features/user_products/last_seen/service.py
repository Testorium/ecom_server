from loguru import logger
from .repo import LastSeenProductRepository


class LastSeenProductService:
    MAX_LAST_SEEN_LENGTH = 10

    def __init__(self, repo: LastSeenProductRepository):
        self.repo = repo

    async def _upsert(self, user_id: int, product_id: int) -> None:
        try:
            await self.repo._upsert(user_id, product_id)

            oldest_ids = await self.repo._fetch_oldest_ids(
                user_id, offset=self.MAX_LAST_SEEN_LENGTH
            )
            await self.repo._delete_by_ids(oldest_ids)

        except Exception:
            logger.exception("Failed to create last seen product record.")
