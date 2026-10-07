from aiogram.types import CallbackQuery, Message, User

from bot.services.errors import get_channel_id, send_error_to_admin
from bot.services.events import log_button
from bot.types import FunctionInlineKeyboard, KeyboardArgs


async def copy_message_from_channel(
    event: CallbackQuery | Message,
    channel: str,
    message_ids: list[int],
    args: KeyboardArgs,
    function_inline_keyboard: FunctionInlineKeyboard,
) -> None:
    bot = event.bot
    user: User | None = event.from_user
    chat_id = event.chat.id if isinstance(event, Message) else event.from_user.id

    try:
        if user is not None:
            await log_button(user, args.button_caption or '')

        channel_id = await get_channel_id(bot, channel)
        if channel_id is None:
            return

        remove_message_ids: list[int] = []
        last_id = 0
        for message_id in message_ids:
            copied = await bot.copy_message(
                chat_id=chat_id,
                from_chat_id=channel_id,
                message_id=message_id,
            )
            last_id = copied.message_id
            remove_message_ids.append(last_id)

        keyboard_args = KeyboardArgs(
            button_caption=args.button_caption,
            remove_message_ids=remove_message_ids,
        )
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=last_id,
            reply_markup=function_inline_keyboard(keyboard_args),
        )
    except Exception as e:  # noqa: BLE001
        await send_error_to_admin(bot, e, chat_id)
    finally:
        if isinstance(event, CallbackQuery):
            await event.answer('')
