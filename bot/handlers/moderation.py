import logging
from html import escape

from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.handlers.start import is_admin
from bot.keyboards.inline_moderation import (
    keyboard_inline_moderation,
    keyboard_inline_moderation_back,
)
from bot.services import (
    broadcast_copy,
    broadcast_text,
    get_bot_id,
    log_button,
)
from config import settings
from consts import (
    ACTION_MODERATION,
    CALLBACK_MOD_BACK,
    CALLBACK_MOD_MAILING_MESSAGE,
    CALLBACK_MOD_MAILING_TEXT,
    CALLBACK_MOD_USERS,
)
from db import get_pool
from db.repositories import UserTelegramRepository

logger = logging.getLogger(__name__)

router = Router()

USERS_LIMIT = 100
USERS_MAX_LEN = 3500

MENU_TEXT = '💻 Модерация'
PROMPT_MESSAGE_TEXT = (
    '✉️ Отправьте одним сообщением номер сообщения из информационного канала '
    '(например: 56).\nЧтобы отменить — нажмите «Назад».'
)
PROMPT_TEXT = (
    '📝 Отправьте одним сообщением текст, который нужно разослать всем '
    'пользователям.\nЧтобы отменить — нажмите «Назад».'
)


class ModerationState(StatesGroup):
    message_id = State()
    text = State()


def _allowed(callback: CallbackQuery) -> bool:
    user = callback.from_user
    return user is not None and is_admin(user.id)


async def _finish(
    state: FSMContext,
    message: Message,
    result: dict,
) -> None:
    data = await state.get_data()
    chat_id = data.get('prompt_chat_id')
    message_id = data.get('prompt_message_id')
    await state.clear()

    text = (
        '✅ Рассылка завершена\n'
        f'👥 Всего: {result["total"]}\n'
        f'📬 Доставлено: {result["ok"]}\n'
        f'🚫 Заблокировали бота: {result["blocked"]}\n'
        f'⚠️ Ошибок: {result["failed"]}'
    )

    try:
        await message.delete()
    except TelegramAPIError:
        logger.debug('Не удалось удалить сообщение модератора')

    if chat_id and message_id:
        try:
            await message.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=keyboard_inline_moderation(),
            )
            return
        except TelegramBadRequest:
            logger.debug('Не удалось обновить сообщение модерации')

    await message.answer(text, reply_markup=keyboard_inline_moderation())


@router.message(F.text == ACTION_MODERATION)
async def handle_moderation(message: Message) -> None:
    if message.from_user is None or not is_admin(message.from_user.id):
        return
    await message.answer(MENU_TEXT, reply_markup=keyboard_inline_moderation())
    try:
        await log_button(message.from_user, message.text or '')
    except Exception:
        logger.exception('Ошибка логирования нажатия кнопки')
    try:
        await message.delete()
    except TelegramBadRequest:
        logger.debug('Не удалось удалить сообщение пользователя')


@router.callback_query(F.data == CALLBACK_MOD_MAILING_MESSAGE)
async def mailing_by_message(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not _allowed(callback) or callback.message is None:
        await callback.answer('⛔ Нет доступа', show_alert=True)
        return
    await state.set_state(ModerationState.message_id)
    await state.update_data(
        prompt_chat_id=callback.message.chat.id,
        prompt_message_id=callback.message.message_id,
    )
    await callback.message.edit_text(
        PROMPT_MESSAGE_TEXT,
        reply_markup=keyboard_inline_moderation_back(),
    )
    await callback.answer()


@router.callback_query(F.data == CALLBACK_MOD_MAILING_TEXT)
async def mailing_by_text(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not _allowed(callback) or callback.message is None:
        await callback.answer('⛔ Нет доступа', show_alert=True)
        return
    await state.set_state(ModerationState.text)
    await state.update_data(
        prompt_chat_id=callback.message.chat.id,
        prompt_message_id=callback.message.message_id,
    )
    await callback.message.edit_text(
        PROMPT_TEXT,
        reply_markup=keyboard_inline_moderation_back(),
    )
    await callback.answer()


@router.message(ModerationState.message_id)
async def capture_message_id(message: Message, state: FSMContext) -> None:
    await state.update_data(value_message_id=message.message_id)
    value = (message.text or '').strip()
    if not value.isdigit():
        await message.answer(
            '🔢 Нужно число. Отправьте номер сообщения, например: 56',
        )
        return
    bot_id = await get_bot_id()
    result = await broadcast_copy(
        message.bot,
        bot_id,
        settings.channel_info,
        int(value),
    )
    await _finish(state, message, result)


@router.message(ModerationState.text)
async def capture_text(message: Message, state: FSMContext) -> None:
    await state.update_data(value_message_id=message.message_id)
    value = message.text or ''
    if not value.strip():
        await message.answer('⚠️ Пустое сообщение. Отправьте текст для рассылки')
        return
    bot_id = await get_bot_id()
    result = await broadcast_text(message.bot, bot_id, value)
    await _finish(state, message, result)


def _user_line(index: int, user) -> str:
    name = ' '.join(p for p in (user.first_name, user.last_name) if p) or 'Без имени'
    link = f'<a href="tg://user?id={user.user_telegram_id}">{escape(name)}</a>'
    username = f' @{escape(user.username)}' if user.username else ''
    return f'{index}. {link}{username}'


@router.callback_query(F.data == CALLBACK_MOD_USERS)
async def list_users(callback: CallbackQuery, state: FSMContext) -> None:
    if not _allowed(callback) or callback.message is None:
        await callback.answer('⛔ Нет доступа', show_alert=True)
        return
    await state.clear()

    bot_id = await get_bot_id()
    users = await UserTelegramRepository(get_pool()).list_by_bot(
        bot_id,
        limit=USERS_LIMIT,
    )

    if not users:
        text = '👥 Пользователей пока нет'
    else:
        lines = [f'👥 Пользователи ({len(users)}):', '']
        length = sum(len(x) for x in lines)
        for index, user in enumerate(users, 1):
            line = _user_line(index, user)
            if length + len(line) > USERS_MAX_LEN:
                lines.append('…')
                break
            lines.append(line)
            length += len(line)
        text = '\n'.join(lines)

    await callback.message.edit_text(
        text,
        reply_markup=keyboard_inline_moderation_back(),
        disable_web_page_preview=True,
    )
    await callback.answer()


@router.callback_query(F.data == CALLBACK_MOD_BACK)
async def back_to_menu(callback: CallbackQuery, state: FSMContext) -> None:
    if not _allowed(callback) or callback.message is None:
        await callback.answer('⛔ Нет доступа', show_alert=True)
        return
    data = await state.get_data()
    value_message_id = data.get('value_message_id')
    await state.clear()
    if value_message_id:
        try:
            await callback.bot.delete_message(
                callback.message.chat.id,
                value_message_id,
            )
        except TelegramAPIError:
            logger.debug('Не удалось удалить сообщение со значением')
    await callback.message.edit_text(
        MENU_TEXT,
        reply_markup=keyboard_inline_moderation(),
    )
    await callback.answer()
