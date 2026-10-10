import asyncio
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.routers import router
from config import settings
from db import close_pool, get_pool, init_pool
from db.migrate import apply_migrations

logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).resolve().parent.parent


async def on_startup(bot: Bot) -> None:
    me = await bot.get_me()
    print(f'Бот @{me.username} запущен. Нажмите Ctrl+C для остановки.')


async def main():
    log_format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    logging.basicConfig(
        level=settings.log_level,
        format=log_format,
    )

    file_handler = RotatingFileHandler(
        ROOT_DIR / 'bot.log',
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8',
    )
    file_handler.setLevel(settings.log_level)
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger('').addHandler(file_handler)

    await init_pool()
    logger.info('Database connected')
    logger.info('DEBUG Target ID from settings: %s', settings.debug_user_id)

    if settings.migrations_auto:
        async with get_pool().acquire() as conn:
            applied = await apply_migrations(conn)
        logger.info('Migrations applied: %s', applied or 'none')

    aiohttp_session = AiohttpSession(proxy=settings.proxy_url or None)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=aiohttp_session,
    )
    logger.info('Bot created (proxy=%s)', bool(settings.proxy_url))

    dp = Dispatcher(storage=MemoryStorage())
    dp.startup.register(on_startup)
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=settings.debug)

    logger.info('Bot started')
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await close_pool()
        logger.info('Bot stopped')


if __name__ == '__main__':
    asyncio.run(main())
