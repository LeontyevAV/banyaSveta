from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.keyboards.inline_reviews import keyboard_inline_reviews
from bot.keyboards.prev import keyboard_inline_prev_message
from bot.services.copy import copy_message_from_channel
from bot.types import KeyboardArgs
from config import settings
from consts import ACTION_INLINE_LEAVE_REVIEWS, ACTION_INLINE_REVIEWS

router = Router()

MESSAGE_IDS_REVIEWS = [62]
MESSAGE_IDS_LEAVE_REVIEWS = [61]


@router.callback_query(F.data == ACTION_INLINE_REVIEWS)
async def handle_reviews(callback: CallbackQuery) -> None:
    await copy_message_from_channel(
        event=callback,
        channel=settings.channel_info,
        message_ids=MESSAGE_IDS_REVIEWS,
        args=KeyboardArgs(button_caption=ACTION_INLINE_REVIEWS),
        function_inline_keyboard=keyboard_inline_reviews,
    )


@router.callback_query(F.data == ACTION_INLINE_LEAVE_REVIEWS)
async def handle_leave_reviews(callback: CallbackQuery) -> None:
    await copy_message_from_channel(
        event=callback,
        channel=settings.channel_info,
        message_ids=MESSAGE_IDS_LEAVE_REVIEWS,
        args=KeyboardArgs(button_caption=ACTION_INLINE_LEAVE_REVIEWS),
        function_inline_keyboard=keyboard_inline_prev_message,
    )
