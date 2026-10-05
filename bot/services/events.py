import logging

from aiogram.types import User

from bot.services.bots import get_bot_id
from db import get_pool
from db.repositories import (
    UserEventRepository,
    UserEventTypeRepository,
    UserTelegramRepository,
)

logger = logging.getLogger(__name__)

EVENT_BUTTON = 'кнопка'


async def log_button(user: User, text: str) -> None:
    pool = get_pool()
    bot_id = await get_bot_id()

    user_row = await UserTelegramRepository(pool).upsert(
        bot_id=bot_id,
        user_telegram_id=user.id,
        username=user.username or '',
        is_bot=user.is_bot,
        first_name=user.first_name,
        last_name=user.last_name,
        language_code=user.language_code,
        is_premium=user.is_premium,
    )

    event_type = await UserEventTypeRepository(pool).get_by_name(EVENT_BUTTON)
    if event_type is None:
        logger.warning('Не найден тип события "%s"', EVENT_BUTTON)
        return

    await UserEventRepository(pool).add(
        userstelegram_id=user_row.id,
        event_type_id=event_type.id,
        text=text,
    )
