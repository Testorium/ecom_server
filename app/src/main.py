from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from src.database import close_db_pool, init_db_pool
from src.routers import main_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db_pool()
    yield
    await close_db_pool()


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)
