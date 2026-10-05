import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from consts import BOT_ADMIN_ID, ERROR_CHANEL_NOT_FOUND

logger = logging.getLogger(__name__)


async def get_channel_id(bot: Bot, chanel_username: str) -> int | None:
    if not chanel_username:
        logger.error(
            ERROR_CHANEL_NOT_FOUND.format(chanelUserName=chanel_username),
        )
        return None
    try:
        chat = await bot.get_chat(chanel_username)
    except TelegramBadRequest:
        logger.error(
            ERROR_CHANEL_NOT_FOUND.format(chanelUserName=chanel_username),
        )
        return None
    return chat.id


async def send_error_to_admin(
    bot: Bot,
    error: Exception,
    user_id: int | None = None,
) -> None:
    logger.exception('Ошибка бота: %s', error)
    text = f'Ошибка бота: {type(error).__name__}: {error}'
    if user_id is not None:
        text += f'\nuser_id: {user_id}'
    try:
        await bot.send_message(BOT_ADMIN_ID, text)
    except Exception:
        logger.exception('Не удалось уведомить администратора')
