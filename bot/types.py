from collections.abc import Callable
from dataclasses import dataclass, field

from aiogram.types import InlineKeyboardMarkup


@dataclass
class KeyboardArgs:
    button_caption: str | None = None
    remove_message_ids: list[int] = field(default_factory=list)


FunctionInlineKeyboard = Callable[[KeyboardArgs], InlineKeyboardMarkup]
