import sys

sys.path.insert(0, '/home/sasha/work/bots/banyaSveta')

from config import settings  # noqa: E402

print('bot_token set:', bool(settings.bot_token))
print('system_token set:', bool(settings.system_token))
print('pg_password set:', bool(settings.pg_password))
print('proxy set:', bool(settings.proxy_url))
print('debug:', settings.debug)
print('debug_user_id:', settings.debug_user_id)
print('bot_name:', settings.bot_name)
print('log_level:', settings.log_level)
print('channel_info:', settings.channel_info)
print('channel_main:', settings.channel_main)
print('channel_url:', settings.channel_url)
