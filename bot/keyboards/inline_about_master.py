from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.prev import get_prev_message_data
from bot.types import KeyboardArgs
from consts import ACTION_INLINE_ASK_QUESTION, ACTION_INLINE_BACK, URL_MASTER


def keyboard_inline_about_master(args: KeyboardArgs) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=ACTION_INLINE_ASK_QUESTION, url=URL_MASTER)
    builder.button(
        text=ACTION_INLINE_BACK,
        callback_data=get_prev_message_data(args.remove_message_ids),
    )
    builder.adjust(1)
    return builder.as_markup()
