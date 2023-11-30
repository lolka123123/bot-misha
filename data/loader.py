from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from database.database import DataBase

# bot = Bot('5226167292:AAFHzB21VU8zGOQ3SKQBke2gyfJNwdtEkIs', parse_mode='HTML')
bot = Bot('6882651878:AAGArCQjw5J0OU_cRVtBhGg1OzysU_WUfQw', parse_mode='HTML')

db = DataBase()

db.create_users_table()
db.create_admin_table()
db.create_ban_table()
db.create_in_searching_table()
db.create_chats_table()
db.create_chat_messages_table()

storage = MemoryStorage()

dp = Dispatcher(storage=storage)
