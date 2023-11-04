from aiogram.filters import BaseFilter
from aiogram.types import Message
from data.loader import db

class IsAdmin(BaseFilter):

    async def __call__(self, message: Message):
        if db.get_admin(message.from_user.id):
            return True
        return False