from datetime import datetime

import asyncpg

from db.models import UserEvent


class UserEventRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def add(
        self,
        userstelegram_id: int,
        event_type_id: int,
        text: str,
        ext_id: str = '',
        date: datetime | None = None,
    ) -> UserEvent:
        row = await self._pool.fetchrow(
            """
            insert into userevents (
                ext_id, user_telegram_id, text, user_event_type_id,
                created_at, updated_at, date
            ) values (
                $1, $2, $3, $4, now(), now(), coalesce($5, now())
            )
            returning *
            """,
            ext_id,
            userstelegram_id,
            text,
            event_type_id,
            date,
        )
        return UserEvent.model_validate(dict(row))

    async def list_by_user(
        self,
        userstelegram_id: int,
        limit: int = 100,
    ) -> list[UserEvent]:
        rows = await self._pool.fetch(
            'select * from userevents '
            'where user_telegram_id = $1 order by id desc limit $2',
            userstelegram_id,
            limit,
        )
        return [UserEvent.model_validate(dict(r)) for r in rows]

    async def list_by_type(
        self,
        event_type_id: int,
        limit: int = 100,
    ) -> list[UserEvent]:
        rows = await self._pool.fetch(
            'select * from userevents '
            'where user_event_type_id = $1 order by id desc limit $2',
            event_type_id,
            limit,
        )
        return [UserEvent.model_validate(dict(r)) for r in rows]
