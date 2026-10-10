import asyncio
import sys
from unittest.mock import AsyncMock

sys.path.insert(0, '/home/sasha/work/bots/banyaSveta')

from aiogram import Bot, Dispatcher  # noqa: E402
from aiogram.fsm.storage.base import StorageKey  # noqa: E402
from aiogram.fsm.storage.memory import MemoryStorage  # noqa: E402
from aiogram.types import Update  # noqa: E402

from bot.handlers.moderation import router  # noqa: E402

ADMIN_ID = 123298974
TOKEN = '123456:AA'


def cb_mailing(update_id: int) -> Update:
    return Update.model_validate(
        {
            'update_id': update_id,
            'callback_query': {
                'id': str(update_id),
                'from': {'id': ADMIN_ID, 'is_bot': False, 'first_name': 'A'},
                'chat_instance': '1',
                'data': 'mod:mailing:text',
                'message': {
                    'message_id': 10,
                    'date': 0,
                    'chat': {'id': ADMIN_ID, 'type': 'private'},
                    'from': {'id': 1, 'is_bot': True, 'first_name': 'bot'},
                    'text': 'Модерация',
                },
            },
        }
    )


def text_message(update_id: int, text: str) -> Update:
    return Update.model_validate(
        {
            'update_id': update_id,
            'message': {
                'message_id': 11,
                'date': 0,
                'chat': {'id': ADMIN_ID, 'type': 'private'},
                'from': {'id': ADMIN_ID, 'is_bot': False, 'first_name': 'A'},
                'text': text,
            },
        }
    )


async def main():
    bot = Bot(token=TOKEN)
    bot.session = AsyncMock()

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    key = StorageKey(bot_id=bot.id, chat_id=ADMIN_ID, user_id=ADMIN_ID)

    await dp.feed_update(bot, cb_mailing(1))
    print('after mailing callback:')
    print('  state =', await storage.get_state(key))
    print('  data  =', await storage.get_data(key))

    await dp.feed_update(bot, text_message(2, 'hello world'))
    print('after typed text:')
    print('  state =', await storage.get_state(key))
    print('  data  =', await storage.get_data(key))

    await bot.session.close()


asyncio.run(main())
