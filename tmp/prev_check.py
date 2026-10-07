import sys

sys.path.insert(0, '/home/sasha/work/bots/banyaSveta')

from bot.keyboards.inline_about_master import (  # noqa: E402
    keyboard_inline_about_master,
)
from bot.keyboards.prev import (  # noqa: E402
    get_prev_message_data,
    parse_prev_message_data,
)
from bot.types import KeyboardArgs  # noqa: E402

args = KeyboardArgs(button_caption='x', remove_message_ids=[100, 101])
kb = keyboard_inline_about_master(args)
for row in kb.inline_keyboard:
    for btn in row:
        payload = btn.callback_data or btn.url or ''
        print(f'{btn.text!r:25} bytes={len(payload.encode())} data={payload!r}')

print('roundtrip:', parse_prev_message_data(get_prev_message_data([5, 6, 7])))
print('default args:', KeyboardArgs())
