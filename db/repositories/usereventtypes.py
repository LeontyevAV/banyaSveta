import asyncpg

from db.models import UserEventType


class UserEventTypeRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def get_by_id(self, type_id: int) -> UserEventType | None:
        row = await self._pool.fetchrow(
            'select * from usereventtypes where id = $1',
            type_id,
        )
        return UserEventType.model_validate(dict(row)) if row else None

    async def get_by_name(self, name: str) -> UserEventType | None:
        row = await self._pool.fetchrow(
            'select * from usereventtypes where name = $1',
            name,
        )
        return UserEventType.model_validate(dict(row)) if row else None

    async def list_all(self) -> list[UserEventType]:
        rows = await self._pool.fetch('select * from usereventtypes order by id')
        return [UserEventType.model_validate(dict(r)) for r in rows]
