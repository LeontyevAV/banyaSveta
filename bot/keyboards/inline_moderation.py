from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from consts import (
    ACTION_INLINE_BACK,
    ACTION_INLINE_MAILING_BY_MESSAGE,
    ACTION_INLINE_MAILING_BY_TEXT,
    ACTION_INLINE_MOD_USERS,
    CALLBACK_MOD_BACK,
    CALLBACK_MOD_MAILING_MESSAGE,
    CALLBACK_MOD_MAILING_TEXT,
    CALLBACK_MOD_USERS,
)


def keyboard_inline_moderation() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=ACTION_INLINE_MAILING_BY_MESSAGE,
        callback_data=CALLBACK_MOD_MAILING_MESSAGE,
    )
    builder.button(
        text=ACTION_INLINE_MAILING_BY_TEXT,
        callback_data=CALLBACK_MOD_MAILING_TEXT,
    )
    builder.button(
        text=ACTION_INLINE_MOD_USERS,
        callback_data=CALLBACK_MOD_USERS,
    )
    builder.adjust(1)
    return builder.as_markup()


def keyboard_inline_moderation_back() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=ACTION_INLINE_BACK, callback_data=CALLBACK_MOD_BACK)
    builder.adjust(1)
    return builder.as_markup()
