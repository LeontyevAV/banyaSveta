import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from bot.handlers.start import is_admin
from bot.keyboards import (
    inline_master_banya_keyboard,
    inline_services_keyboard,
    keyboard_inline_certificate,
    keyboard_inline_prev_message,
    keyboard_inline_subscribe_channel,
)
from bot.services import copy_message_from_channel, log_button, user_is_subscribed
from bot.types import KeyboardArgs
from config import settings
from consts import (
    ACTION_ABOUT_MASTER_BANYA,
    ACTION_CERTIFICATE,
    ACTION_GET_PRESENT,
    ACTION_MODERATION,
    ACTION_SERVICES,
)

logger = logging.getLogger(__name__)

router = Router()

MESSAGE_IDS_CERTIFICATE = [64]
MESSAGE_IDS_GET_PRESENT = [65]

GET_PRESENT_SUBSCRIBE_TEXT = (
    'Чтобы получить подарок, подпишитесь на канал «БАНЯ СВЕТА» 🤗\n'
    'и снова нажмите «Получить подарок»'
)

MODERATION_HELP_TEXT = (
    '# users - список всех пользователей\n'
    '# post 13_59_02_04_2026  # messageId_56 - отложенное сообщение\n'
    '  на 13:59 02.04.2026 с ИД 56 (В РАЗРАБОТКЕ)\n'
    '# messageId_56 - мгновенное сообщение с ид 56\n'
    '# text Привет )) - мгновенное сообщение с заданным текстом'
)


@router.message(F.text == ACTION_SERVICES)
async def handle_services(message: Message) -> None:
    await message.answer(
        'Какая информация вас интересует?',
        reply_markup=inline_services_keyboard(),
    )
    try:
        await log_button(message.from_user, message.text or '')
    except Exception:
        logger.exception('Ошибка логирования нажатия кнопки')
    try:
        await message.delete()
    except TelegramBadRequest:
        logger.debug('Не удалось удалить сообщение пользователя')


@router.message(F.text == ACTION_ABOUT_MASTER_BANYA)
async def handle_about_master_banya(message: Message) -> None:
    await message.answer(
        'Выберите заинтересовавший вас пункт',
        reply_markup=inline_master_banya_keyboard(),
    )
    try:
        await log_button(message.from_user, message.text or '')
    except Exception:
        logger.exception('Ошибка логирования нажатия кнопки')
    try:
        await message.delete()
    except TelegramBadRequest:
        logger.debug('Не удалось удалить сообщение пользователя')


@router.message(F.text == ACTION_CERTIFICATE)
async def handle_certificate(message: Message) -> None:
    await copy_message_from_channel(
        event=message,
        channel=settings.channel_info,
        message_ids=MESSAGE_IDS_CERTIFICATE,
        args=KeyboardArgs(button_caption=ACTION_CERTIFICATE),
        function_inline_keyboard=keyboard_inline_certificate,
    )
    try:
        await message.delete()
    except TelegramBadRequest:
        logger.debug('Не удалось удалить сообщение пользователя')


@router.message(F.text == ACTION_GET_PRESENT)
async def handle_get_present(message: Message) -> None:
    if message.from_user is None:
        return

    if await user_is_subscribed(
        message.bot,
        settings.channel_main,
        message.from_user.id,
    ):
        await copy_message_from_channel(
            event=message,
            channel=settings.channel_info,
            message_ids=MESSAGE_IDS_GET_PRESENT,
            args=KeyboardArgs(button_caption=ACTION_GET_PRESENT),
            function_inline_keyboard=keyboard_inline_prev_message,
        )
        try:
            await message.delete()
        except TelegramBadRequest:
            logger.debug('Не удалось удалить сообщение пользователя')
        return

    try:
        await log_button(message.from_user, ACTION_GET_PRESENT)
    except Exception:
        logger.exception('Ошибка логирования нажатия кнопки')
    sent = await message.answer(GET_PRESENT_SUBSCRIBE_TEXT)
    await sent.edit_reply_markup(
        reply_markup=keyboard_inline_subscribe_channel(
            KeyboardArgs(remove_message_ids=[sent.message_id]),
        ),
    )


@router.message(F.text == ACTION_MODERATION)
async def handle_moderation(message: Message) -> None:
    if message.from_user is None or not is_admin(message.from_user.id):
        return
    await message.answer(MODERATION_HELP_TEXT)
    try:
        await log_button(message.from_user, ACTION_MODERATION)
    except Exception:
        logger.exception('Ошибка логирования нажатия кнопки')
    try:
        await message.delete()
    except TelegramBadRequest:
        logger.debug('Не удалось удалить сообщение пользователя')
