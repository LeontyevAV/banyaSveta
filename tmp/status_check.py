import asyncio
import sys

sys.path.insert(0, '/home/sasha/work/bots/banyaSveta')

import asyncpg  # noqa: E402

from config import settings  # noqa: E402


async def main():
    conn = await asyncpg.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        database=settings.pg_database,
        user=settings.pg_username,
        password=settings.pg_password,
    )
    for bot_id in (1, 2, 4):
        rows = await conn.fetch(
            'select id, user_telegram_id, username, status '
            'from userstelegram where bot_id = $1 order by id',
            bot_id,
        )
        print(f'bot_id={bot_id}:')
        for r in rows:
            print('   ', dict(r))
    await conn.close()


asyncio.run(main())
