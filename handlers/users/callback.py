from datetime import timedelta

from data.loader import bot, dp, db
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from data.translate import get_translate

from states.states import states
from handlers.users.text_handlers import show_main_menu

from keyboards.reply import reply_keyboard
from keyboards.inline import inline_keyboard


from time import sleep

import requests

router = Router()

@router.callback_query(F.data == 'cansel')
async def main_searching_delete_message(call: CallbackQuery, state: FSMContext):
    lang = db.get_user(call.from_user.id)[3]
    if db.get_user_from_searching(call.from_user.id):
        data = await state.get_data()
        message_id = data['message_id']
        await bot.edit_message_text(text=get_translate(lang, 'main_searching_cansel_text'),
                                    chat_id=call.message.chat.id, message_id=message_id)
        db.remove_user_from_searching(call.message.chat.id)
        await state.clear()
        await show_main_menu(call.message, state)
    else:
        await call.message.delete()

@router.callback_query(F.data == 'close_message')
async def close_message(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

@router.callback_query(F.data == 'settings')
async def profile_message(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    lang = db.get_user(call.message.chat.id)[3]
    got_state = await state.get_state()
    if got_state != states.MainStates.searching and got_state != states.MainStates.chatting:
        await state.set_state(states.MainMenu.settings_menu)
        await call.message.answer(get_translate(lang, 'menu_settings_button'),
                                  reply_markup=reply_keyboard.settings_menu(lang))

@router.callback_query(F.data.startswith('like'))
async def like_user(call: CallbackQuery, state: FSMContext):
    lang = db.get_user(call.message.chat.id)[3]
    chat_id = int(call.data.split('_')[1])

    db.change_user_stats(chat_id, likes=1, rating=1)

    await call.message.edit_text(get_translate(lang, 'main_chatting_liked_text'))

@router.callback_query(F.data.startswith('dislike'))
async def dislike_user(call: CallbackQuery, state: FSMContext):
    lang = db.get_user(call.message.chat.id)[3]
    chat_id = int(call.data.split('_')[1])

    db.change_user_stats(chat_id, dislikes=1, rating=-1)

    await call.message.edit_text(get_translate(lang, 'main_chatting_liked_text'))




# from handlers.users.text_handlers import show_main_menu
#
#
# @dp.callback_query(lambda call: call.data == 'cansel', state=states.MainMenu.main_menu)
# async def main_searching_delete_message(call: CallbackQuery):
#     await call.message.delete()
#
# @dp.callback_query(lambda call: call.data == 'cansel', state=states.MainStates.searching)
# async def main_searching(call: CallbackQuery, state: FSMContext):
#     lang = db.get_user(call.message.chat.id)[3]
#     async with state.proxy() as data:
#         message_id = data['message_id']
#         await bot.edit_message_text(text=get_translate(lang, 'main_searching_cansel_text'),
#                                     chat_id=call.message.chat.id, message_id=message_id)
#         db.remove_user_from_searching(call.message.chat.id)
#         await state.finish()
#         await show_main_menu(call.message)


