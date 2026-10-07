from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.prev import get_prev_message_data
from bot.types import KeyboardArgs
from consts import ACTION_INLINE_LEAVE_REVIEWS, ACTION_INLINE_PREV_MESSAGE


def keyboard_inline_reviews(args: KeyboardArgs) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=ACTION_INLINE_LEAVE_REVIEWS,
        callback_data=ACTION_INLINE_LEAVE_REVIEWS,
    )
    builder.button(
        text=ACTION_INLINE_PREV_MESSAGE,
        callback_data=get_prev_message_data(args.remove_message_ids),
    )
    builder.adjust(1)
    return builder.as_markup()
