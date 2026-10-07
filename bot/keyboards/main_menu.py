from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from consts import (
    ACTION_ABOUT_MASTER_BANYA,
    ACTION_CERTIFICATE,
    ACTION_GET_PRESENT,
    ACTION_MODERATION,
    ACTION_SERVICES,
)


def main_menu_keyboard(is_admin: bool = False) -> ReplyKeyboardMarkup:
    rows = [
        [
            KeyboardButton(text=ACTION_ABOUT_MASTER_BANYA),
            KeyboardButton(text=ACTION_SERVICES),
        ],
        [
            KeyboardButton(text=ACTION_CERTIFICATE),
            KeyboardButton(text=ACTION_GET_PRESENT),
        ],
    ]
    if is_admin:
        rows.append([KeyboardButton(text=ACTION_MODERATION)])

    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
    )
