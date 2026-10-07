from aiogram import Router

from bot.handlers import (
    about,
    contacts,
    menu,
    navigation,
    reviews,
    services,
    start,
)

router = Router()
router.include_router(start.router)
router.include_router(menu.router)
router.include_router(services.router)
router.include_router(reviews.router)
router.include_router(contacts.router)
router.include_router(about.router)
router.include_router(navigation.router)

__all__ = ['router']
