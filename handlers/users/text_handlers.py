from data.loader import bot, dp, db
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import StateFilter

from data.translate import get_translate, get_languages
from states.states import states
from keyboards.reply import reply_keyboard
from keyboards.inline import inline_keyboard
# from handlers.users.commands import commands

from filters.is_admin import IsAdmin

router = Router()

import time

# @dp.message()
# async def start(message: Message, state: FSMContext):
#     await state.set_state(states.RegistrationState.choose_language)
#     await message.answer('Выберите язык:\nChoose language:',
#                          reply_markup=reply_keyboard.choose_language())




@router.message(StateFilter(None))
async def start(message: Message, state: FSMContext):
    if db.get_user(message.chat.id):

        await show_main_menu(message, state)
    else:
        await state.set_state(states.RegistrationState.choose_language)
        await message.answer('Выберите язык:\nChoose language:',
                             reply_markup=reply_keyboard.choose_language())

    # chat_id = message.chat.id
    # date = message.date.timestamp()
    # user_banned = db.get_banned_user(chat_id)
    #
    # if user_banned:
    #     if user_banned[2] <= date:
    #         db.remove_ban_user(chat_id)
    #         await start(message)
    #     else:
    #         text = f'Ваш аккаунт был заблокирован!\nОсталось: {int(user_banned[2] - date)} секунд\nКем: @{user_banned[3]}'
    #         await message.answer(text)
    #
    # else:
    #     if db.get_user(message.chat.id):
    #         await show_main_menu(message, state)
    #     else:
    #         await state.set_state(states.RegistrationState.choose_language)
    #         await message.answer('Выберите язык:\nChoose language:',
    #                              reply_markup=reply_keyboard.choose_language())


@router.message(states.RegistrationState.choose_language)
async def registration_choose_language(message: Message, state: FSMContext):
    for key, value in get_languages().items():
        if message.text == key:
            await state.update_data(language=value)
            await state.set_state(states.RegistrationState.choose_gender)
            await message.answer(get_translate(value, 'registration_choose_gender_text'),
                                 reply_markup=reply_keyboard.choose_gender(value))


@router.message(states.RegistrationState.choose_gender)
async def registration_choose_gender(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['language']

    if message.text == get_translate(lang, 'gender_male_button'):
        db.add_user(telegram_id=message.chat.id,
                    username=message.from_user.username,
                    gender='male',
                    language=lang)
        await state.clear()
        await show_main_menu(message, state)
    elif message.text == get_translate(lang, 'gender_female_button'):
        db.add_user(telegram_id=message.chat.id,
                    username=message.from_user.username,
                    gender='female',
                    language=lang)
        await state.clear()
        await show_main_menu(message, state)

from aiogram.fsm.storage.base import StorageKey
async def show_main_menu(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]
    await state.set_state(states.MainMenu.main_menu)
    # state_with: FSMContext = FSMContext(storage=dp.storage, key=StorageKey(chat_id=message.chat.id,
    #                                                                        user_id=message.from_user.id,
    #                                                                        bot_id=bot.id))
    # await state_with.set_state(states.MainMenu.main_menu)
    await message.answer(get_translate(lang, 'menu_show_text'), reply_markup=reply_keyboard.main_menu(lang))

@router.message(states.MainMenu.main_menu)
async def main_menu(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]

    if message.text == get_translate(lang, 'menu_start_button'):
        db.add_user_in_searching(message.from_user.id, message.date.timestamp())
        await state.clear()
        await state.set_state(states.MainStates.searching)

        msg_remove_keyboard = await bot.send_message(chat_id=message.chat.id, text='.',
                                                     reply_markup=ReplyKeyboardRemove())
        await bot.delete_message(chat_id=message.chat.id, message_id=msg_remove_keyboard.message_id)

        msg = await message.answer(get_translate(lang, 'main_searching_text'),
                                   reply_markup=inline_keyboard.searching(lang))
        await state.update_data(message_id=msg.message_id)



    elif message.text == get_translate(lang, 'menu_settings_button'):
        await state.set_state(states.MainMenu.settings_menu)
        await message.answer(get_translate(lang, 'menu_settings_button'),
                             reply_markup=reply_keyboard.settings_menu(lang))

    elif message.text == get_translate(lang, 'menu_info_button'):
        await message.answer(get_translate(lang, 'menu_info_text'))





# -----Настройки
@router.message(states.MainMenu.settings_menu)
async def settings_menu(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]


    if message.text == get_translate(lang, 'main_back_button'):
        await state.clear()
        await show_main_menu(message, state)

    elif message.text == get_translate(lang, 'settings_change_language_button'):
        await state.set_state(states.SettingsChangeLanguage.choose_language)
        await message.answer('Выберите язык:\nChoose language:',
                             reply_markup=reply_keyboard.choose_language())

@router.message(states.SettingsChangeLanguage.choose_language)
async def settings_choose_language(message: Message, state: FSMContext):
    for key, value in get_languages().items():
        if message.text == key:
            db.change_user_language_by_telegram_id(message.chat.id, value)
            await state.clear()
            await show_main_menu(message, state)

# -----Настройки


@dp.message(states.MainStates.chatting)
async def main_chatting(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]
    data = await state.get_data()
    chat = data['chat']

    another_user = chat[1]
    if another_user == message.chat.id:
        another_user = chat[2]

    if len(message.text) > 255:
        await message.answer(get_translate(lang, 'main_chatting_words_limit_text'))
    else:
        db.add_chat_message(chat_id=chat[0], telegram_id=message.from_user.id,
                            message_text=message.text,
                            date=message.date.timestamp())
        await bot.send_message(chat_id=another_user, text=message.text)


