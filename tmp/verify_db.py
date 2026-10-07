import asyncio
import sys

sys.path.insert(0, '/home/leontyevav/work/bots/banyaSveta')

from bot.services.bots import get_bot_id  # noqa: E402
from db import close_pool, get_pool, init_pool  # noqa: E402
from db.repositories import (  # noqa: E402
    UserEventRepository,
    UserEventTypeRepository,
    UserTelegramRepository,
)

TEST_USER_ID = 999888777


async def main():
    await init_pool()
    pool = get_pool()
    bot_id = await get_bot_id()
    print('bot_id =', bot_id)

    repo = UserTelegramRepository(pool)
    row = await repo.upsert(
        bot_id=bot_id,
        user_telegram_id=TEST_USER_ID,
        username='verify_db',
        first_name='Verify',
    )
    print('upsert ok, row id =', row.id, 'created_at =', row.created_at)

    event_type = await UserEventTypeRepository(pool).get_by_name('кнопка')
    event = await UserEventRepository(pool).add(
        userstelegram_id=row.id,
        event_type_id=event_type.id,
        text='verify',
        ext_id='0',
    )
    print('event ok, id =', event.id, 'created_at =', event.created_at)

    try:
        await pool.execute('delete from userevents where id = $1', event.id)
        await pool.execute('delete from userstelegram where id = $1', row.id)
        print('cleanup ok')
    finally:
        await close_pool()


asyncio.run(main())
