import sys

sys.path.insert(0, '/home/sasha/work/bots/banyaSveta')

from bot.keyboards import inline_master_banya_keyboard  # noqa: E402

kb = inline_master_banya_keyboard()
for row in kb.inline_keyboard:
    for btn in row:
        data = btn.callback_data or btn.url or ''
        print(f'{btn.text!r:45} bytes={len(data.encode())}  data={data!r}')
