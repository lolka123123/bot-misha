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
from middlewares.antiflood import AntiFloodMiddleware
import handlers

db.create_users_table()
db.create_admin_table()
db.create_ban_table()
db.create_in_searching_table()
db.create_in_chatting_table()
db.create_chats_table()
db.create_chat_messages_table()



async def auto_searching():
    while True:
        in_searching = db.get_users_from_searching_after_seconds(int(time.time()))
        count = len(in_searching)

        if count >= 2:
            user1 = in_searching[random.randint(1, count) - 1][0]
            user2 = in_searching[random.randint(1, count) - 1][0]
            while user1 == user2:
                user2 = in_searching[random.randint(1, count) - 1][0]

            db.remove_user_from_searching(user1)
            db.remove_user_from_searching(user2)

            db.add_chat(user1, user2, int(time.time()))

            chat = db.get_last_chat()

            db.add_in_chatting(user1, chat[0])
            db.add_in_chatting(user2, chat[0])

            user1_state: FSMContext = FSMContext(storage=dp.storage,
                                                 key=StorageKey(chat_id=user1, user_id=user1, bot_id=bot.id))
            user2_state: FSMContext = FSMContext(storage=dp.storage,
                                                 key=StorageKey(chat_id=user2, user_id=user2, bot_id=bot.id))

            await user1_state.set_state(states.MainStates.chatting)
            await user2_state.set_state(states.MainStates.chatting)

            user1_lang = db.get_user(user1)[3]
            user2_lang = db.get_user(user2)[3]

            await user1_state.update_data(chat=chat)
            await user2_state.update_data(chat=chat)

            user1_data = await user1_state.get_data()
            user2_data = await user2_state.get_data()

            await bot.edit_message_text(get_translate(user1_lang, 'main_chatting_is_found_text'), chat_id=user1,
                                        message_id=user1_data['message_id'])
            await bot.edit_message_text(get_translate(user2_lang, 'main_chatting_is_found_text'), chat_id=user2,
                                        message_id=user2_data['message_id'])

        else:
            await asyncio.sleep(5)

async def on_shutdown():
    for i in db.get_users_from_searching():
        await bot.send_message(chat_id=i[0], text='Бот отключен')
    for i in db.get_users_from_chatting():
        await bot.send_message(chat_id=i[0], text='Бот отключен')

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    db.remove_all_users_from_searching()
    db.remove_all_users_from_chatting()
    # dp.message.middleware(AntiFloodMiddleware())


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
        loop = asyncio.get_event_loop()
        task1 = loop.create_task(main())
        task2 = loop.create_task(auto_searching())
        loop.run_until_complete(asyncio.wait([task1, task2]))

        # asyncio.run(main())
    except:
        print('done')