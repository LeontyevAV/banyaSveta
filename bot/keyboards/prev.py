from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.types import KeyboardArgs
from consts import ACTION_INLINE_BACK

PREV_PREFIX = 'prev:'


def get_prev_message_data(remove_message_ids: list[int]) -> str:
    return PREV_PREFIX + ','.join(str(i) for i in remove_message_ids)


def parse_prev_message_data(data: str) -> list[int]:
    if not data.startswith(PREV_PREFIX):
        return []
    rest = data[len(PREV_PREFIX) :]
    return [int(x) for x in rest.split(',') if x]


def keyboard_inline_prev_message(args: KeyboardArgs) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=ACTION_INLINE_BACK,
        callback_data=get_prev_message_data(args.remove_message_ids),
    )
    builder.adjust(1)
    return builder.as_markup()
