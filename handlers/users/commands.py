import timestamp as timestamp
from aiogram.fsm.storage.base import StorageKey

from data.loader import bot, dp, db

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command



from states.states import states
from keyboards.reply import reply_keyboard
from data.translate import get_translate
from data.config import show_time, check_time
from filters.is_admin import IsAdmin


import datetime

# router = Router()

@dp.message(Command('stop'), states.MainStates.chatting)
async def stop_chatting(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]
    data = await state.get_data()
    chat = data['chat']

    another_user = chat[1]
    if another_user == message.from_user.id:
        another_user = chat[2]

    db.remove_user_from_chatting(message.from_user.id)
    db.remove_user_from_chatting(another_user)

    another_user_lang = db.get_user(another_user)[3]

    another_user_state: FSMContext = FSMContext(storage=dp.storage,
                                                key=StorageKey(chat_id=another_user, user_id=another_user, bot_id=bot.id))

    await state.clear()
    await another_user_state.clear()

    await state.set_state(states.MainMenu.main_menu)
    await another_user_state.set_state(states.MainMenu.main_menu)

    await bot.send_message(chat_id=message.from_user.id, text=get_translate(lang, 'main_chatting_finished_text'))
    await bot.send_message(chat_id=another_user, text=get_translate(another_user_lang, 'main_chatting_finished_text'))

    await bot.send_message(chat_id=message.from_user.id, text=get_translate(lang, 'menu_show_text'),
                           reply_markup=reply_keyboard.main_menu(lang))
    await bot.send_message(chat_id=another_user, text=get_translate(another_user_lang, 'menu_show_text'),
                           reply_markup=reply_keyboard.main_menu(another_user_lang))


@dp.message(Command('check'), IsAdmin(), states.MainStates.chatting)
async def check_chat(message: Message, state:FSMContext):
    lang = db.get_user(message.from_user.id)[3]
    data = await state.get_data()
    chat = data['chat']
    timestamp = datetime.datetime.fromtimestamp(message.date.timestamp())
    time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    await message.answer(f'<b>chat_id:</b> {chat[0]}\n<b>first_user_id:</b> {chat[1]}\n<b>second_user_id:</b> {chat[2]}\n<b>time:</b> {time}')

# MainMenu:main_menu
# async def commands(message: Message, *args):
#     # if message.text.split(' ')[0] == '/start':
#     #     await states.MainMenu.main_menu.set()
#     #     await args[0](message)
#
#     # ------------admin_commands------------
#     elif message.text.split(' ')[0] == '/admin':
#         lang = db.get_user(message.chat.id)[3]
#         chat_id = message.chat.id
#         if not db.get_admin(chat_id):
#             await message.answer(get_translate(lang, 'admin_no_access'))
#         else:
#             command = message.text.split(' ')[1:]
#             print(message)
#
#
#     elif message.text.split(' ')[0] == '/ban':
#         lang = db.get_user(message.chat.id)[3]
#         chat_id = message.chat.id
#         if not db.get_admin(chat_id):
#             await message.answer(get_translate(lang, 'admin_no_access'))
#         else:
#             command = message.text.split(' ')[1:]
#             if message.text.split(' ')[0] == '/ban':
#                 if command == list():
#                     await message.answer('/ban <b>(username) (time) (reason)</b>')
#                 else:
#                     username = command[0][1:]
#                     user = db.get_user_by_username(username)
#                     if not user:
#                         await message.answer('Пользователь не найден')
#                     else:
#                         if db.get_banned_user(user[0]):
#                             await message.answer('Пользователь находится в блокировке')
#                         else:
#                             try:
#
#                                 time = check_time(command[1])
#                                 if time < 0 or not time:
#                                     await message.answer('Не корректно указано время')
#                                 else:
#                                     try:
#                                         reason = command[2]
#                                     except:
#                                         reason = ''
#
#                                     db.add_user_to_ban(telegram_id=user[0],
#                                                        date=message.date.timestamp(),
#                                                        to_date=int(message.date.timestamp()) + time,
#                                                        who_banned=message.from_user.username,
#                                                        reason=reason)
#
#                                     text = f'@{user[1]} был заблокирован!\nВремя: {show_time(time)}\nКем: @{message.from_user.username}'
#                                     text2 = f'Ваш аккаунт был заблокирован!\nВремя: {show_time(time)}\nКем: @{message.from_user.username}'
#                                     if reason != '':
#                                         text += f'\nПричина: {reason}'
#                                         text2 += f'\nПричина: {reason}'
#                                     await message.answer(text)
#                                     await bot.send_message(chat_id=user[0],
#                                                            text=text2)
#
#                             except IndexError:
#                                 await message.answer('Укажите время')
#
#
#     elif message.text.split(' ')[0] == '/unban':
#         lang = db.get_user(message.chat.id)[3]
#         chat_id = message.chat.id
#         if not db.get_admin(chat_id):
#             await message.answer(get_translate(lang, 'admin_no_access'))
#         else:
#             command = message.text.split(' ')[1:]
#
#             if command == list():
#                 await message.answer('/unban <b>(username)</b>')
#             else:
#                 username = command[0][1:]
#                 user = db.get_user_by_username(username)
#
#                 if not user:
#                     await message.answer('Пользователь не найден')
#                 else:
#                     if not db.get_banned_user(user[0]):
#                         await message.answer('Пользователь не находится в блокировке')
#                     else:
#                         db.remove_ban_user(user[0])
#                         await message.answer(f'@{user[1]} разблокирован!')
#                         await message.answer(f'Вы были разблокированы!')
#
#     else:
#         await message.answer('Такой команды не существует')
#
