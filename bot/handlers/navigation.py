import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from bot.keyboards.inline_about_master import (
    PREV_PREFIX,
    parse_prev_message_data,
)

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data.startswith(PREV_PREFIX))
async def handle_prev_message(callback: CallbackQuery) -> None:
    await callback.answer('')

    message_ids = parse_prev_message_data(callback.data or '')
    for message_id in message_ids:
        try:
            await callback.bot.delete_message(callback.from_user.id, message_id)
        except TelegramBadRequest:
            logger.debug('Не удалось удалить сообщение %s', message_id)
