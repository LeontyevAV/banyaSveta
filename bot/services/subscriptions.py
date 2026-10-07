import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

logger = logging.getLogger(__name__)

SUBSCRIBED_STATUSES = {'creator', 'administrator', 'member'}


async def user_is_subscribed(bot: Bot, channel: str, user_id: int) -> bool:
    if not channel:
        logger.error('Не задан основной канал для проверки подписки')
        return False
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    except TelegramBadRequest:
        logger.exception('Не удалось проверить подписку на %s', channel)
        return False
    return member.status in SUBSCRIBED_STATUSES
