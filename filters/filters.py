from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from data.loader import bot, dp, db

from states.states import states

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message):
        if db.get_admin(message.from_user.id):
            return True
        return False

class CommandStartFilter(BaseFilter):
    async def __call__(self, message: Message):
        state: FSMContext = FSMContext(storage=dp.storage,
                                       key=StorageKey(chat_id=message.chat.id, user_id=message.from_user.id,
                                                      bot_id=bot.id))
        got_state = await state.get_state()
        if got_state != states.MainStates.searching and got_state != states.MainStates.chatting:
            return True
        return False