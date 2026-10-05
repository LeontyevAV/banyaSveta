import asyncpg

from config import settings

_pool: asyncpg.Pool | None = None


async def init_pool(
    min_size: int = 1,
    max_size: int = 10,
) -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            host=settings.pg_host,
            port=settings.pg_port,
            database=settings.pg_database,
            user=settings.pg_username,
            password=settings.pg_password,
            min_size=min_size,
            max_size=max_size,
        )
    return _pool


def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError('Пул не инициализирован. Вызовите init_pool() при старте.')
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
