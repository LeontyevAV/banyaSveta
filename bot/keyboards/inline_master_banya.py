from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from consts import (
    ACTION_INLINE_ABOUT_BANYA,
    ACTION_INLINE_ABOUT_MASTER,
    ACTION_INLINE_ASK_QUESTION,
    ACTION_INLINE_CONTACTS,
    ACTION_INLINE_LEAVE_REVIEWS,
    ACTION_INLINE_REVIEWS,
    URL_MASTER,
)


def inline_master_banya_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=ACTION_INLINE_ABOUT_MASTER,
        callback_data=ACTION_INLINE_ABOUT_MASTER,
    )
    builder.button(
        text=ACTION_INLINE_ABOUT_BANYA,
        callback_data=ACTION_INLINE_ABOUT_BANYA,
    )
    builder.button(
        text=ACTION_INLINE_REVIEWS,
        callback_data=ACTION_INLINE_REVIEWS,
    )
    builder.button(
        text=ACTION_INLINE_LEAVE_REVIEWS,
        callback_data=ACTION_INLINE_LEAVE_REVIEWS,
    )
    builder.button(
        text=ACTION_INLINE_ASK_QUESTION,
        url=URL_MASTER,
    )
    builder.button(
        text=ACTION_INLINE_CONTACTS,
        callback_data=ACTION_INLINE_CONTACTS,
    )
    builder.adjust(1)
    return builder.as_markup()
