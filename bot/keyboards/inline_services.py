from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from consts import (
    ACTION_INLINE_BANYA_ON_LITE,
    ACTION_INLINE_BOOKING_RULES,
    ACTION_INLINE_CERTIFICATE,
    ACTION_INLINE_HARMONY_IN_COUPLE,
    ACTION_INLINE_REGISTER,
    ACTION_INLINE_SCHEDULE,
    ACTION_INLINE_TOTAL_CARE,
    ACTION_INLINE_WARM_INSIDE,
    URL_MASTER,
)


def inline_services_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=ACTION_INLINE_WARM_INSIDE,
        callback_data=ACTION_INLINE_WARM_INSIDE,
    )
    builder.button(
        text=ACTION_INLINE_HARMONY_IN_COUPLE,
        callback_data=ACTION_INLINE_HARMONY_IN_COUPLE,
    )
    builder.button(
        text=ACTION_INLINE_TOTAL_CARE,
        callback_data=ACTION_INLINE_TOTAL_CARE,
    )
    builder.button(
        text=ACTION_INLINE_BANYA_ON_LITE,
        callback_data=ACTION_INLINE_BANYA_ON_LITE,
    )
    builder.button(
        text=ACTION_INLINE_CERTIFICATE,
        callback_data=ACTION_INLINE_CERTIFICATE,
    )
    builder.button(
        text=ACTION_INLINE_SCHEDULE,
        callback_data=ACTION_INLINE_SCHEDULE,
    )
    builder.button(
        text=ACTION_INLINE_BOOKING_RULES,
        callback_data=ACTION_INLINE_BOOKING_RULES,
    )
    builder.button(
        text=ACTION_INLINE_REGISTER,
        url=URL_MASTER,
    )
    builder.adjust(1)
    return builder.as_markup()
