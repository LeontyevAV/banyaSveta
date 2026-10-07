from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.prev import get_prev_message_data
from bot.types import KeyboardArgs
from config import settings
from consts import ACTION_INLINE_PREV_MESSAGE, ACTION_INLINE_SUBSCRIBE_CHANNEL


def keyboard_inline_subscribe_channel(args: KeyboardArgs) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=ACTION_INLINE_SUBSCRIBE_CHANNEL,
        url=settings.channel_url,
    )
    builder.button(
        text=ACTION_INLINE_PREV_MESSAGE,
        callback_data=get_prev_message_data(args.remove_message_ids),
    )
    builder.adjust(1)
    return builder.as_markup()
