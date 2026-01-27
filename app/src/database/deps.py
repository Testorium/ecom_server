from typing import Annotated

from asyncpg import Pool
from fastapi import Depends

from .pool import get_db_pool

DatabasePoolDep = Annotated[Pool, Depends(get_db_pool)]
