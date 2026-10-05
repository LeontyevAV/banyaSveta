import asyncpg

from db.models import Bot


class BotRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def get_by_id(self, bot_id: int) -> Bot | None:
        row = await self._pool.fetchrow(
            'select * from bots where id = $1',
            bot_id,
        )
        return Bot.model_validate(dict(row)) if row else None

    async def get_by_name(self, name: str) -> Bot | None:
        row = await self._pool.fetchrow(
            'select * from bots where name = $1',
            name,
        )
        return Bot.model_validate(dict(row)) if row else None

    async def resolve_id(self, name: str) -> int:
        bot_id = await self._pool.fetchval(
            'select id from bots where name = $1',
            name,
        )
        if bot_id is None:
            raise ValueError(f'Бот "{name}" не найден в таблице bots')
        return bot_id

    async def list_all(self) -> list[Bot]:
        rows = await self._pool.fetch('select * from bots order by id')
        return [Bot.model_validate(dict(r)) for r in rows]
