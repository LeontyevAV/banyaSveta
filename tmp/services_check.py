import sys

sys.path.insert(0, '/home/sasha/work/bots/banyaSveta')

from bot.keyboards import inline_services_keyboard  # noqa: E402

kb = inline_services_keyboard()
for row in kb.inline_keyboard:
    for btn in row:
        data = btn.callback_data or btn.url or ''
        flag = '  <-- OVER 64!' if len(data.encode()) > 64 else ''
        print(f'{len(data.encode()):3} bytes  {btn.text!r}{flag}')
