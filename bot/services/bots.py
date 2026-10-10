from config import settings
from db import get_pool
from db.repositories import BotRepository

_bot_id: int | None = None


async def get_bot_id() -> int:
    global _bot_id
    if _bot_id is None:
        _bot_id = await BotRepository(get_pool()).resolve_id(
            settings.bot_name_effective,
        )
    return _bot_id
