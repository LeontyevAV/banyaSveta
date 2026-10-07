from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.keyboards.inline_certificate import keyboard_inline_certificate
from bot.keyboards.inline_service_info import keyboard_inline_service_info
from bot.keyboards.prev import keyboard_inline_prev_message
from bot.services.copy import copy_message_from_channel
from bot.types import KeyboardArgs
from config import settings
from consts import (
    ACTION_INLINE_BANYA_ON_LITE,
    ACTION_INLINE_BOOKING_RULES,
    ACTION_INLINE_CERTIFICATE,
    ACTION_INLINE_HARMONY_IN_COUPLE,
    ACTION_INLINE_SCHEDULE,
    ACTION_INLINE_TOTAL_CARE,
    ACTION_INLINE_WARM_INSIDE,
)

router = Router()

MESSAGE_IDS_WARM_INSIDE = [52]
MESSAGE_IDS_HARMONY_IN_COUPLE = [53]
MESSAGE_IDS_TOTAL_CARE = [54]
MESSAGE_IDS_BANYA_ON_LITE = [78]
MESSAGE_IDS_SCHEDULE = [63]
MESSAGE_IDS_BOOKING_RULES = [46]
MESSAGE_IDS_CERTIFICATE = [64]


@router.callback_query(F.data == ACTION_INLINE_WARM_INSIDE)
async def handle_warm_inside(callback: CallbackQuery) -> None:
    await copy_message_from_channel(
        event=callback,
        channel=settings.channel_info,
        message_ids=MESSAGE_IDS_WARM_INSIDE,
        args=KeyboardArgs(button_caption=ACTION_INLINE_WARM_INSIDE),
        function_inline_keyboard=keyboard_inline_service_info,
    )


@router.callback_query(F.data == ACTION_INLINE_HARMONY_IN_COUPLE)
async def handle_harmony_in_couple(callback: CallbackQuery) -> None:
    await copy_message_from_channel(
        event=callback,
        channel=settings.channel_info,
        message_ids=MESSAGE_IDS_HARMONY_IN_COUPLE,
        args=KeyboardArgs(button_caption=ACTION_INLINE_HARMONY_IN_COUPLE),
        function_inline_keyboard=keyboard_inline_service_info,
    )


@router.callback_query(F.data == ACTION_INLINE_TOTAL_CARE)
async def handle_total_care(callback: CallbackQuery) -> None:
    await copy_message_from_channel(
        event=callback,
        channel=settings.channel_info,
        message_ids=MESSAGE_IDS_TOTAL_CARE,
        args=KeyboardArgs(button_caption=ACTION_INLINE_TOTAL_CARE),
        function_inline_keyboard=keyboard_inline_service_info,
    )


@router.callback_query(F.data == ACTION_INLINE_BANYA_ON_LITE)
async def handle_banya_on_lite(callback: CallbackQuery) -> None:
    await copy_message_from_channel(
        event=callback,
        channel=settings.channel_info,
        message_ids=MESSAGE_IDS_BANYA_ON_LITE,
        args=KeyboardArgs(button_caption=ACTION_INLINE_BANYA_ON_LITE),
        function_inline_keyboard=keyboard_inline_service_info,
    )


@router.callback_query(F.data == ACTION_INLINE_SCHEDULE)
async def handle_schedule(callback: CallbackQuery) -> None:
    await copy_message_from_channel(
        event=callback,
        channel=settings.channel_info,
        message_ids=MESSAGE_IDS_SCHEDULE,
        args=KeyboardArgs(button_caption=ACTION_INLINE_SCHEDULE),
        function_inline_keyboard=keyboard_inline_service_info,
    )


@router.callback_query(F.data == ACTION_INLINE_BOOKING_RULES)
async def handle_booking_rules(callback: CallbackQuery) -> None:
    await copy_message_from_channel(
        event=callback,
        channel=settings.channel_info,
        message_ids=MESSAGE_IDS_BOOKING_RULES,
        args=KeyboardArgs(button_caption=ACTION_INLINE_BOOKING_RULES),
        function_inline_keyboard=keyboard_inline_prev_message,
    )


@router.callback_query(F.data == ACTION_INLINE_CERTIFICATE)
async def handle_certificate(callback: CallbackQuery) -> None:
    await copy_message_from_channel(
        event=callback,
        channel=settings.channel_info,
        message_ids=MESSAGE_IDS_CERTIFICATE,
        args=KeyboardArgs(button_caption=ACTION_INLINE_CERTIFICATE),
        function_inline_keyboard=keyboard_inline_certificate,
    )
