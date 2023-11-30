from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from data.loader import bot, dp, db

import time
import random
from states.states import states
from data.translate import get_translate, get_profile_to_premium_text, get_profile_without_premium_text
import asyncio



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

            user1_profile = db.get_user_to_profile(user1)
            user2_profile = db.get_user_to_profile(user2)



            await bot.edit_message_text(text=get_translate(user1_lang, 'main_chatting_is_found_text'),
                                        chat_id=user1,
                                        message_id=user1_data['message_id'])
            await bot.edit_message_text(text=get_translate(user2_lang, 'main_chatting_is_found_text'),
                                        chat_id=user2,
                                        message_id=user2_data['message_id'])

            if db.get_premium(user1):
                await bot.send_message(chat_id=user1, text=get_profile_to_premium_text(lang=user1_lang,
                                                                                       likes=user2_profile[0],
                                                                                       dislikes=user2_profile[1],
                                                                                       rating=user2_profile[2],
                                                                                       country=user2_profile[4],
                                                                                       gender=user2_profile[3],
                                                                                       age=user2_profile[6],
                                                                                       interests=user2_profile[7],
                                                                                       language=user2_profile[5]))
            else:
                await bot.send_message(chat_id=user1, text=get_profile_without_premium_text(lang=user1_lang,
                                                                                            likes=user2_profile[0],
                                                                                            dislikes=user2_profile[1],
                                                                                            rating=user2_profile[2]))
            if db.get_premium(user2):
                msg = await bot.send_message(chat_id=user2, text=get_profile_to_premium_text(lang=user2_lang,
                                                                                             likes=user1_profile[0],
                                                                                             dislikes=user1_profile[1],
                                                                                             rating=user1_profile[2],
                                                                                             country=user1_profile[4],
                                                                                             gender=user1_profile[3],
                                                                                             age=user1_profile[6],
                                                                                             interests=user1_profile[7],
                                                                                             language=user1_profile[5]))
            else:
                msg = await bot.send_message(chat_id=user2, text=get_profile_without_premium_text(lang=user2_lang,
                                                                                                  likes=user1_profile[0],
                                                                                                  dislikes=user1_profile[1],
                                                                                                  rating=user1_profile[2]))

            await user1_state.update_data(message=msg, sent_messages=0, sent_photos=0, sent_videos=0,
                                          sent_videos_note=0, sent_stickers=0, sent_voices=0, sent_audios=0,
                                          sent_document=0, time_spent_in_chatting=0)
            await user2_state.update_data(message=msg, sent_messages=0, sent_photos=0, sent_videos=0,
                                          sent_videos_note=0, sent_stickers=0, sent_voices=0, sent_audios=0,
                                          sent_document=0, time_spent_in_chatting=0)

        else:
            await asyncio.sleep(5)

