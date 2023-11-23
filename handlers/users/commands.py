import timestamp as timestamp
from aiogram.fsm.storage.base import StorageKey

from data.loader import bot, dp, db

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandObject



from states.states import states
from keyboards.reply import reply_keyboard
from data.translate import get_translate
from data.config import show_time, check_time
from filters.is_admin import IsAdmin


import datetime

# router = Router()


async def stop_chatting_def(user1, user2):
    db.remove_user_from_chatting(user1)
    db.remove_user_from_chatting(user2)

    user1_lang = db.get_user(user1)[3]
    user2_lang = db.get_user(user2)[3]

    user1_state: FSMContext = FSMContext(storage=dp.storage,
                                         key=StorageKey(chat_id=user1, user_id=user1, bot_id=bot.id))
    user2_state: FSMContext = FSMContext(storage=dp.storage,
                                         key=StorageKey(chat_id=user2, user_id=user2, bot_id=bot.id))

    await user1_state.clear()
    await user2_state.clear()

    await user1_state.set_state(states.MainMenu.main_menu)
    await user2_state.set_state(states.MainMenu.main_menu)

    await bot.send_message(chat_id=user1, text=get_translate(user1_lang, 'main_chatting_finished_text'))
    await bot.send_message(chat_id=user2, text=get_translate(user2_lang, 'main_chatting_finished_text'))

    await bot.send_message(chat_id=user1, text=get_translate(user1_lang, 'menu_show_text'),
                           reply_markup=reply_keyboard.main_menu(user1_lang))
    await bot.send_message(chat_id=user2, text=get_translate(user2_lang, 'menu_show_text'),
                           reply_markup=reply_keyboard.main_menu(user2_lang))


@dp.message(Command('stop'), states.MainStates.chatting)
async def stop_chatting(message: Message, state: FSMContext):
    data = await state.get_data()
    chat = data['chat']

    another_user = chat[1]
    if another_user == message.from_user.id:
        another_user = chat[2]

    await stop_chatting_def(message.from_user.id, another_user)


@dp.message(Command('check'), IsAdmin(), states.MainStates.chatting)
async def check_chat(message: Message, state:FSMContext):
    lang = db.get_user(message.from_user.id)[3]
    data = await state.get_data()
    chat = data['chat']
    timestamp = datetime.datetime.fromtimestamp(message.date.timestamp())
    time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    await message.answer(f'<b>chat_id:</b> {chat[0]}\n<b>first_user_id:</b> {chat[1]}\n<b>second_user_id:</b> {chat[2]}\n<b>time:</b> {time}')

@dp.message(Command('ban'), IsAdmin())
async def command_ban(message: Message, state: FSMContext, command: CommandObject):
    lang = db.get_user(message.from_user.id)[3]
    if command.args is None:
        await message.answer('/ban <b>(username) (time) (reason)</b>')
    else:
        command = command.args.split(' ')

        try:
            user_id = int(command[0])
            user = db.get_user(user_id)
        except:
            if command[0][0] == '@':
                username = command[0][1:]
            else:
                username = command[0]
            user = db.get_user_by_username(username)

        if not user:
            await message.answer('Пользователь не найден')
        else:

            if db.get_banned_user(user[0]):
                await message.answer('Пользователь находится в блокировке')
            else:
                try:

                    time = check_time(command[1])
                    if time < 0 or not time:
                        await message.answer('Не корректно указано время')
                    else:
                        try:
                            reason = command[2]
                        except:
                            reason = ''

                        db.add_user_to_ban(telegram_id=user[0],
                                           date=message.date.timestamp(),
                                           to_date=int(message.date.timestamp()) + time,
                                           who_banned=message.from_user.username,
                                           reason=reason)


                        text = f'@{user[1]} был заблокирован!\nВремя: {show_time(time)}\nКем: @{message.from_user.username}'
                        text2 = f'Ваш аккаунт был заблокирован!\nВремя: {show_time(time)}\nКем: @{message.from_user.username}'
                        if reason != '':
                            text += f'\nПричина: {reason}'
                            text2 += f'\nПричина: {reason}'

                        user_state: FSMContext = FSMContext(storage=dp.storage,
                                                            key=StorageKey(chat_id=user[0], user_id=user[0],
                                                                           bot_id=bot.id))

                        if db.get_user_from_searching(user[0]):
                            data = await user_state.get_data()
                            message_id = data['message_id']
                            await bot.edit_message_text(text=get_translate(lang, 'main_searching_cansel_text'),
                                                        chat_id=user[0], message_id=message_id)
                            db.remove_user_from_searching(user[0])
                            await user_state.clear()

                        elif db.get_user_from_chatting(user[0]):
                            data = await user_state.get_data()
                            chat = data['chat']
                            await stop_chatting_def(chat[1], chat[2])


                        await message.answer(text)
                        await bot.send_message(chat_id=user[0],
                                               text=text2)

                except IndexError:
                    await message.answer('Укажите время')


@dp.message(Command('unban'), IsAdmin())
async def command_unban(message: Message, state: FSMContext, command: CommandObject):
    lang = db.get_user(message.from_user.id)[3]
    if command.args is None:
        await message.answer('/unban <b>(username)</b>')
    else:
        command = command.args.split(' ')

        try:
            user_id = int(command[0])
            user = db.get_user(user_id)
        except:
            if command[0][0] == '@':
                username = command[0][1:]
            else:
                username = command[0]
            user = db.get_user_by_username(username)


        if not user:
            await message.answer('Пользователь не найден')
        else:
            if not db.get_banned_user(user[0]):
                await message.answer('Пользователь не находится в блокировке')
            else:
                try:
                    reason = command[1]
                except:
                    reason = ''

                text = f'Вы были разблокированы!\nКем: @{message.from_user.username}'
                if reason != '':
                    text += f'\nПричина: {reason}'

                db.remove_ban_user(user[0])

                await message.answer(f'@{user[1]} разблокирован!')

                await bot.send_message(chat_id=user[0], text=text)





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
