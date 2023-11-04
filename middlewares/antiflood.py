from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Callable, Awaitable, Dict, Any
from cachetools import TTLCache
# cachetools
class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, time_limit: int=1):
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        if event.chat.id in self.limit:
            return
        self.limit[event.chat.id] = None
        return await handler(event, data)


