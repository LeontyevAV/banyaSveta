from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.main_menu import main_menu_keyboard
from consts import BOT_ADMIN_ID, BOT_CONTENT_START_TEXT, BOT_MODERATOR_ID

router = Router()

ADMIN_IDS = {BOT_ADMIN_ID, BOT_MODERATOR_ID}


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        BOT_CONTENT_START_TEXT,
        reply_markup=main_menu_keyboard(is_admin(message.from_user.id)),
    )
