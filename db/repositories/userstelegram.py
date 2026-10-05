import asyncpg

from db.models import UserTelegram


class UserTelegramRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def get_by_telegram_id(
        self,
        bot_id: int,
        user_telegram_id: int,
    ) -> UserTelegram | None:
        row = await self._pool.fetchrow(
            'select * from userstelegram where bot_id = $1 and user_telegram_id = $2',
            bot_id,
            user_telegram_id,
        )
        return UserTelegram.model_validate(dict(row)) if row else None

    async def upsert(
        self,
        bot_id: int,
        user_telegram_id: int,
        username: str = '',
        is_bot: bool = False,
        first_name: str | None = None,
        last_name: str | None = None,
        language_code: str | None = None,
        is_premium: bool | None = None,
        photo_id: int | None = None,
        status: str | None = None,
    ) -> UserTelegram:
        row = await self._pool.fetchrow(
            """
            insert into userstelegram (
                bot_id, user_telegram_id, username, is_bot,
                first_name, last_name, language_code, is_premium,
                photo_id, status, created_at, updated_at
            ) values (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, now(), now()
            )
            on conflict (user_telegram_id, bot_id) do update set
                username = excluded.username,
                is_bot = excluded.is_bot,
                first_name = excluded.first_name,
                last_name = excluded.last_name,
                language_code = excluded.language_code,
                is_premium = excluded.is_premium,
                photo_id = coalesce(excluded.photo_id, userstelegram.photo_id),
                status = coalesce(excluded.status, userstelegram.status),
                updated_at = now()
            returning *
            """,
            bot_id,
            user_telegram_id,
            username or '',
            is_bot,
            first_name,
            last_name,
            language_code,
            is_premium,
            photo_id,
            status,
        )
        return UserTelegram.model_validate(dict(row))

    async def set_status(self, row_id: int, status: str) -> None:
        await self._pool.execute(
            'update userstelegram set status = $1, updated_at = now() where id = $2',
            status,
            row_id,
        )

    async def set_photo_id(self, row_id: int, photo_id: int) -> None:
        await self._pool.execute(
            'update userstelegram set photo_id = $1, updated_at = now() where id = $2',
            photo_id,
            row_id,
        )

    async def list_by_bot(self, bot_id: int, limit: int = 100) -> list[UserTelegram]:
        rows = await self._pool.fetch(
            'select * from userstelegram where bot_id = $1 order by id desc limit $2',
            bot_id,
            limit,
        )
        return [UserTelegram.model_validate(dict(r)) for r in rows]
