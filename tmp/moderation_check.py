import sys

sys.path.insert(0, '/home/sasha/work/bots/banyaSveta')

from bot.keyboards.inline_moderation import (  # noqa: E402
    keyboard_inline_moderation,
    keyboard_inline_moderation_back,
)

print('menu:')
for row in keyboard_inline_moderation().inline_keyboard:
    for b in row:
        print('  ', b.text, '|', b.callback_data)
print('back:')
for row in keyboard_inline_moderation_back().inline_keyboard:
    for b in row:
        print('  ', b.text, '|', b.callback_data)
