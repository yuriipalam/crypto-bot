from typing import Any, Awaitable, Callable, Dict, MutableMapping

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache

THROTTLE_TIME = 7


class ThrottlingMiddleware(BaseMiddleware):
    caches = TTLCache(maxsize=10_000, ttl=THROTTLE_TIME)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        if event.chat.id in self.caches:
            await event.answer("Relax dude...")
            return

        self.caches[event.chat.id] = None
        return await handler(event, data)
