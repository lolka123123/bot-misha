import asyncio
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from data.loader import bot, dp, db
from data.translate import get_translate
from states.states import states
import random
import time
from middlewares.middlewares import *
import handlers
from asyncdef.auto_searching import auto_searching

db.create_users_table()
db.create_users_stats_table()
db.create_admin_table()
db.create_ban_table()
db.create_in_searching_table()
db.create_in_chatting_table()
db.create_chats_table()
db.create_chat_messages_table()
db.create_premium_table()

db.create_test()




async def on_shutdown():
    for i in db.get_users_from_searching():
        await bot.send_message(chat_id=i[0], text='Бот отключен')
    for i in db.get_users_from_chatting():
        await bot.send_message(chat_id=i[0], text='Бот отключен')

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    db.remove_all_users_from_searching()
    db.remove_all_users_from_chatting()
    dp.message.middleware(BannedUserMiddleware())
    dp.message.middleware(ChangeUsernameMiddleware())
    dp.message.middleware(PremiumMiddleware())



    dp.include_routers(
        handlers.users.text_handlers.router,
        handlers.users.callback.router,
    )
    print('start')
    # await dp.shutdown(auto_searching())
    await dp.start_polling(bot)

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.create_task(auto_searching())
    try:
        # loop = asyncio.get_event_loop()
        # task1 = loop.create_task(main())
        # # task2 = loop.create_task(auto_searching())
        # loop.run_until_complete(asyncio.wait([task1]))

        asyncio.run(main())
    except:
        print('done')