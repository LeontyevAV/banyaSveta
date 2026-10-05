import asyncio
import sys

BASE = '/home/sasha/work/bots/banyaSveta'
sys.path.insert(0, BASE)

from config import settings  # noqa: E402
from db import close_pool, init_pool  # noqa: E402
from db.repositories import (  # noqa: E402
    BotRepository,
    UserEventTypeRepository,
)


async def main():
    pool = await init_pool()
    bots = BotRepository(pool)
    types = UserEventTypeRepository(pool)

    print('settings.bot_name =', settings.bot_name)
    print('settings.pg =', settings.pg_host, settings.pg_port, settings.pg_database)
    print('pg_password loaded =', bool(settings.pg_password))

    bot_id = await bots.resolve_id(settings.bot_name)
    print('resolved bot_id =', bot_id)

    print('bots:')
    for b in await bots.list_all():
        print('  ', b.id, b.name, b.ext_bot_id)

    print('event types:')
    for t in await types.list_all():
        print('  ', t.id, t.name)

    us = bot_id
    from db.repositories import UserTelegramRepository  # noqa: E402

    ut = UserTelegramRepository(pool)
    found = await ut.list_by_bot(bot_id, limit=5)
    print(f'userstelegram (bot_id={bot_id}): {len(found)} rows')
    for u in found:
        print('  ', u.id, u.user_telegram_id, u.username, u.status)

    await close_pool()
    print('OK')


asyncio.run(main())
