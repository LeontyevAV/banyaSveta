import sys

sys.path.insert(0, '/home/leontyevav/work/bots/banyaSveta')

from bot.keyboards import (  # noqa: E402
    keyboard_inline_certificate,
    keyboard_inline_contacts,
    keyboard_inline_prev_message,
    keyboard_inline_reviews,
    keyboard_inline_service_info,
    keyboard_inline_subscribe_channel,
)
from bot.handlers import services  # noqa: E402,F401
from bot.routers import router  # noqa: E402,F401
from bot.types import KeyboardArgs  # noqa: E402

args = KeyboardArgs(
    button_caption='🚶🏼 Перейти на канал',
    remove_message_ids=[100, 101],
)
for name, factory in (
    ('service_info', keyboard_inline_service_info),
    ('certificate', keyboard_inline_certificate),
    ('prev', keyboard_inline_prev_message),
    ('subscribe', keyboard_inline_subscribe_channel),
    ('reviews', keyboard_inline_reviews),
    ('contacts', keyboard_inline_contacts),
):
    print(f'--- {name} ---')
    kb = factory(args)
    for row in kb.inline_keyboard:
        for btn in row:
            data = btn.callback_data or btn.url or ''
            flag = '  <-- OVER 64!' if len(data.encode()) > 64 else ''
            print(f'{len(data.encode()):3} bytes  {btn.text!r}{flag}')
