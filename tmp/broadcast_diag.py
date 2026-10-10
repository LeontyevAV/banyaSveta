import asyncio
import sys

sys.path.insert(0, '/home/sasha/work/bots/banyaSveta')

import asyncpg  # noqa: E402
from aiogram import Bot  # noqa: E402
from aiogram.client.default import DefaultBotProperties  # noqa: E402
from aiogram.client.session.aiohttp import AiohttpSession  # noqa: E402
from aiogram.enums import ParseMode  # noqa: E402

from config import settings  # noqa: E402

RECIPIENTS = (
    'select count(*) from userstelegram '
    "where bot_id = $1 and coalesce(status, 'member') "
    "not in ('bot_is_blocked', 'left', 'kicked')"
)


async def main():
    print('debug =', settings.debug)
    print('bot_name =', settings.bot_name)
    print('bot_name_test =', settings.bot_name_test)
    print('bot_name_effective =', settings.bot_name_effective)
    print('channel_info =', settings.channel_info)
    print('channel_main =', settings.channel_main)

    conn = await asyncpg.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        database=settings.pg_database,
        user=settings.pg_username,
        password=settings.pg_password,
    )
    print('\nbots:')
    for r in await conn.fetch('select id, name from bots order by id'):
        cnt = await conn.fetchval(RECIPIENTS, r['id'])
        total = await conn.fetchval(
            'select count(*) from userstelegram where bot_id = $1', r['id']
        )
        print(f"  id={r['id']} {r['name']}  recipients={cnt}  total={total}")

    for name in (settings.bot_name, settings.bot_name_test):
        bid = await conn.fetchval('select id from bots where name = $1', name)
        print(f'  resolve {name} -> {bid}')
    await conn.close()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=AiohttpSession(proxy=settings.proxy_url or None),
    )
    try:
        me = await bot.get_me()
        print('\nbot token -> @%s (id %s)' % (me.username, me.id))
        try:
            chat = await bot.get_chat(settings.channel_info)
            print('get_chat(%s) -> id=%s type=%s' % (settings.channel_info, chat.id, chat.type))
        except Exception as e:
            print('get_chat(%s) FAILED: %r' % (settings.channel_info, e))
    finally:
        await bot.session.close()


asyncio.run(main())
