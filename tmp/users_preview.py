import asyncio
import sys

sys.path.insert(0, '/home/sasha/work/bots/banyaSveta')

from bot.handlers.moderation import _user_line  # noqa: E402
from db import close_pool, get_pool, init_pool  # noqa: E402
from db.repositories import UserTelegramRepository  # noqa: E402


async def main():
    await init_pool()
    repo = UserTelegramRepository(get_pool())
    for bot_id in (1, 2):
        users = await repo.list_by_bot(bot_id, limit=100)
        print(f'--- bot_id={bot_id} ({len(users)}) ---')
        for i, u in enumerate(users, 1):
            print(' ', _user_line(i, u))
    await close_pool()


asyncio.run(main())
