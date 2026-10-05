import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from bot.keyboards import inline_master_banya_keyboard
from bot.services import log_button
from consts import (
    ACTION_ABOUT_MASTER_BANYA,
    ACTION_CERTIFICATE,
    ACTION_GET_PRESENT,
    ACTION_MODERATION,
    ACTION_SERVICES,
)

logger = logging.getLogger(__name__)

router = Router()

STUB_TEXT = '🚧 Раздел в разработке'


@router.message(F.text == ACTION_SERVICES)
async def handle_services(message: Message) -> None:
    await message.answer(STUB_TEXT)


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
    await message.answer(STUB_TEXT)


@router.message(F.text == ACTION_GET_PRESENT)
async def handle_get_present(message: Message) -> None:
    await message.answer(STUB_TEXT)


@router.message(F.text == ACTION_MODERATION)
async def handle_moderation(message: Message) -> None:
    await message.answer(STUB_TEXT)
