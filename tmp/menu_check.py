import sys

sys.path.insert(0, '/home/sasha/work/bots/banyaSveta')

from bot.keyboards.main_menu import main_menu_keyboard  # noqa: E402

for admin in (False, True):
    kb = main_menu_keyboard(admin)
    print(f'--- is_admin={admin} ---')
    for row in kb.keyboard:
        print('  ', [b.text for b in row])
