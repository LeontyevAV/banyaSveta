from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.keyboards.inline_contacts import keyboard_inline_contacts
from bot.services.copy import copy_message_from_channel
from bot.services.subscriptions import user_is_subscribed
from bot.types import KeyboardArgs
from config import settings
from consts import (
    ACTION_INLINE_CONTACTS,
    ACTION_INLINE_GOTO_CHANEL,
    ACTION_INLINE_SUBSCRIBE_CHANNEL,
)

router = Router()

MESSAGE_IDS_CONTACTS = [55]


@router.callback_query(F.data == ACTION_INLINE_CONTACTS)
async def handle_contacts(callback: CallbackQuery) -> None:
    subscribed = await user_is_subscribed(
        callback.bot,
        settings.channel_main,
        callback.from_user.id,
    )
    caption = (
        ACTION_INLINE_GOTO_CHANEL if subscribed else ACTION_INLINE_SUBSCRIBE_CHANNEL
    )
    await copy_message_from_channel(
        event=callback,
        channel=settings.channel_info,
        message_ids=MESSAGE_IDS_CONTACTS,
        args=KeyboardArgs(button_caption=caption),
        function_inline_keyboard=keyboard_inline_contacts,
    )
