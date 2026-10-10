import asyncio
import logging
from collections.abc import Awaitable, Callable

from aiogram import Bot
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramRetryAfter,
)

from db import get_pool
from db.repositories import UserTelegramRepository

logger = logging.getLogger(__name__)

RATE = 20
DELAY = 1 / RATE

RECIPIENTS_QUERY = (
    'select id, user_telegram_id from userstelegram '
    "where bot_id = $1 and coalesce(status, 'member') "
    "not in ('bot_is_blocked', 'left', 'kicked')"
)

SendCall = Callable[[int], Awaitable[object]]


async def _deliver(send: Callable[[], Awaitable[object]]) -> str:
    try:
        await send()
        return 'ok'
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        try:
            await send()
            return 'ok'
        except TelegramForbiddenError:
            return 'blocked'
        except TelegramBadRequest:
            return 'bad'
        except Exception:
            logger.exception('Повторная отправка не удалась')
            return 'failed'
    except TelegramForbiddenError:
        return 'blocked'
    except TelegramBadRequest:
        return 'bad'
    except Exception:
        logger.exception('Отправка не удалась')
        return 'failed'


async def _broadcast(bot_id: int, make_send: SendCall) -> dict:
    pool = get_pool()
    repo = UserTelegramRepository(pool)
    rows = await pool.fetch(RECIPIENTS_QUERY, bot_id)

    counters = {'ok': 0, 'blocked': 0, 'bad': 0, 'failed': 0}
    for row in rows:
        result = await _deliver(lambda uid=row['user_telegram_id']: make_send(uid))
        counters[result] += 1
        if result == 'blocked':
            await repo.set_status(row['id'], 'bot_is_blocked')
        elif result == 'bad':
            await repo.set_status(row['id'], 'left')
        await asyncio.sleep(DELAY)

    return {
        'total': len(rows),
        'ok': counters['ok'],
        'blocked': counters['blocked'],
        'failed': counters['bad'] + counters['failed'],
    }


async def broadcast_text(bot: Bot, bot_id: int, text: str) -> dict:
    return await _broadcast(
        bot_id,
        lambda uid: bot.send_message(uid, text),
    )


async def broadcast_copy(
    bot: Bot,
    bot_id: int,
    channel: str,
    message_id: int,
) -> dict:
    return await _broadcast(
        bot_id,
        lambda uid: bot.copy_message(
            chat_id=uid,
            from_chat_id=channel,
            message_id=message_id,
        ),
    )
