from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.keyboards.inline_about_master import keyboard_inline_about_master
from bot.services.copy import copy_message_from_channel
from bot.types import KeyboardArgs
from config import settings
from consts import ACTION_INLINE_ABOUT_BANYA, ACTION_INLINE_ABOUT_MASTER

router = Router()

MESSAGE_IDS_ABOUT_MASTER = [57, 58]
MESSAGE_IDS_ABOUT_BANYA = [51]


@router.callback_query(F.data == ACTION_INLINE_ABOUT_MASTER)
async def handle_about_master(callback: CallbackQuery) -> None:
    await copy_message_from_channel(
        callback=callback,
        channel=settings.channel_info,
        message_ids=MESSAGE_IDS_ABOUT_MASTER,
        args=KeyboardArgs(button_caption=ACTION_INLINE_ABOUT_MASTER),
        function_inline_keyboard=keyboard_inline_about_master,
    )


@router.callback_query(F.data == ACTION_INLINE_ABOUT_BANYA)
async def handle_about_banya(callback: CallbackQuery) -> None:
    await copy_message_from_channel(
        callback=callback,
        channel=settings.channel_info,
        message_ids=MESSAGE_IDS_ABOUT_BANYA,
        args=KeyboardArgs(button_caption=ACTION_INLINE_ABOUT_BANYA),
        function_inline_keyboard=keyboard_inline_about_master,
    )
