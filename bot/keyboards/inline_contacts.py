from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.prev import get_prev_message_data
from bot.types import KeyboardArgs
from config import settings
from consts import ACTION_INLINE_BACK, ACTION_INLINE_CONTACT, URL_MASTER


def keyboard_inline_contacts(args: KeyboardArgs) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=ACTION_INLINE_CONTACT, url=URL_MASTER)
    builder.button(text=args.button_caption or '', url=settings.channel_url)
    builder.button(
        text=ACTION_INLINE_BACK,
        callback_data=get_prev_message_data(args.remove_message_ids),
    )
    builder.adjust(2)
    return builder.as_markup()
