import sys

sys.path.insert(0, '/home/sasha/work/bots/banyaSveta')

from config import settings  # noqa: E402

print('debug =', settings.debug)
print('bot_name =', settings.bot_name)
print('bot_name_test =', settings.bot_name_test)
print('effective =', settings.bot_name_effective)
