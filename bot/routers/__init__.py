from aiogram import Router

from bot.handlers import about, menu, navigation, start

router = Router()
router.include_router(start.router)
router.include_router(menu.router)
router.include_router(about.router)
router.include_router(navigation.router)

__all__ = ['router']
