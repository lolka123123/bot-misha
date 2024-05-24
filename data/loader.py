from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from database.database import DataBase
from data.config import TELEGRAM_TOKEN



bot = Bot(TELEGRAM_TOKEN, parse_mode='HTML')

bot = Bot('TOKEN', parse_mode='HTML')


db = DataBase()

db.create_users_table()
db.create_admin_table()
db.create_ban_table()
db.create_in_searching_table()
db.create_chats_table()
db.create_chat_messages_table()

storage = MemoryStorage()

dp = Dispatcher(storage=storage)
