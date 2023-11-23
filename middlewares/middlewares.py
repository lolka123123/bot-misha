from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Callable, Awaitable, Dict, Any
from cachetools import TTLCache

from data.loader import bot, db
# cachetools
class BannedUserMiddleware(BaseMiddleware):
    def __init__(self, time_limit: int=10):
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        user_banned = db.get_banned_user(event.from_user.id)
        if not user_banned:
            self.limit[event.chat.id] = None
            return await handler(event, data)
        else:
            if user_banned[2] <= event.date.timestamp():
                db.remove_ban_user(event.from_user.id)
                self.limit[event.chat.id] = None
                return await handler(event, data)
            if event.chat.id in self.limit:
                return
            else:
                self.limit[event.chat.id] = None
            date = event.date.timestamp()
            text = f'Ваш аккаунт был заблокирован!\nОсталось: {int(user_banned[2] - date)} секунд\nКем: @{user_banned[3]}'
            await bot.send_message(chat_id=event.from_user.id, text=text)

class ChangeUsernameMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        user = db.get_user(event.from_user.id)
        if user:
            if user[1] != event.from_user.username:
                db.change_username_by_telegram_id(event.from_user.username)
        return await handler(event, data)
