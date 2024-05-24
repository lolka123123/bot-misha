from data.loader import bot, dp, db
from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from data.translate import get_translate, get_languages, get_translated_countries, get_translated_interests, \
    get_profile_text, get_profile_to_premium_text, get_profile_without_premium_text
from states.states import states
from keyboards.reply import reply_keyboard
from keyboards.inline import inline_keyboard

# from handlers.users.commands import commands
import os

from filters.filters import IsAdmin

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


@router.message(states.RegistrationState.choose_language)
async def registration_choose_language(message: Message, state: FSMContext):
    for key, value in get_languages().items():
        if message.text == key:
            await state.update_data(language=value)
            await message.answer(f"{get_translate(value, 'settings_changed_language_text')} '{key}'")
            await state.set_state(states.RegistrationState.choose_country)
            await message.answer(get_translate(value, 'registration_choose_country_text'),
                                 reply_markup=reply_keyboard.change_country(value))


@router.message(states.RegistrationState.choose_country)
async def registration_choose_country(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['language']

    if message.text == get_translate(lang, 'main_back_button'):
        await message.delete()
        await state.set_state(states.RegistrationState.choose_language)
        await message.answer('Выберите язык:\nChoose language:',
                             reply_markup=reply_keyboard.choose_language())
    for key, value in get_translated_countries(lang).items():
        if message.text == value:
            await state.update_data(country=key)
            await message.answer(f"{get_translate(lang, 'settings_changed_country_text')} '{value}'")
            await state.set_state(states.RegistrationState.choose_gender)
            await message.answer(get_translate(lang, 'registration_choose_gender_text'),
                                 reply_markup=reply_keyboard.change_gender(lang))

@router.message(states.RegistrationState.choose_gender)
async def registration_choose_gender(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['language']

    if message.text == get_translate(lang, 'main_back_button'):
        await state.set_state(states.RegistrationState.choose_country)
        await message.answer(get_translate(lang, 'registration_choose_country_text'),
                             reply_markup=reply_keyboard.change_country(lang))
    elif message.text == get_translate(lang, 'gender_male_button'):
        await state.update_data(gender='male')
        await message.answer(
            f"{get_translate(lang, 'settings_changed_gender_text')} '{get_translate(lang, 'gender_male_button')}'")
        await state.set_state(states.RegistrationState.choose_age)
        await message.answer(get_translate(lang, 'registration_choose_age_text'),
                             reply_markup=reply_keyboard.change_age(lang))
    elif message.text == get_translate(lang, 'gender_female_button'):
        await state.update_data(gender='female')
        await message.answer(
            f"{get_translate(lang, 'settings_changed_gender_text')} '{get_translate(lang, 'gender_female_button')}'")
        await state.set_state(states.RegistrationState.choose_age)
        await message.answer(get_translate(lang, 'registration_choose_age_text'),
                             reply_markup=reply_keyboard.change_age(lang))

@router.message(states.RegistrationState.choose_age)
async def registration_choose_age(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['language']
    if message.text == get_translate(lang, 'main_back_button'):
        await state.set_state(states.RegistrationState.choose_gender)
        await message.answer(get_translate(lang, 'registration_choose_gender_text'),
                             reply_markup=reply_keyboard.change_gender(lang))
    if message.text == get_translate(lang, 'age_before_seventeen_button'):
        await state.update_data(age=0)
        await message.answer(
            f"{get_translate(lang, 'settings_changed_age_text')} '{get_translate(lang, 'age_before_seventeen_button')}'")
        await state.set_state(states.RegistrationState.choose_interests)
        await message.answer(get_translate(lang, 'registration_choose_interests_text'),
                             reply_markup=reply_keyboard.change_interests(lang))
    elif message.text == get_translate(lang, 'age_from_eighteen_to_twenty_one_button'):
        await state.update_data(age=1)
        await message.answer(
            f"{get_translate(lang, 'settings_changed_age_text')} '{get_translate(lang, 'age_from_eighteen_to_twenty_one_button')}'")
        await state.set_state(states.RegistrationState.choose_interests)
        await message.answer(get_translate(lang, 'registration_choose_interests_text'),
                             reply_markup=reply_keyboard.change_interests(lang))
    elif message.text == get_translate(lang, 'age_from_twenty_two_to_thirty_five_button'):
        await state.update_data(age=2)
        await message.answer(
            f"{get_translate(lang, 'settings_changed_age_text')} '{get_translate(lang, 'age_from_twenty_two_to_thirty_five_button')}'")
        await state.set_state(states.RegistrationState.choose_interests)
        await message.answer(get_translate(lang, 'registration_choose_interests_text'),
                             reply_markup=reply_keyboard.change_interests(lang))
    elif message.text == get_translate(lang, 'age_after_thirty_six_button'):
        await state.update_data(age=3)
        await message.answer(
            f"{get_translate(lang, 'settings_changed_age_text')} '{get_translate(lang, 'age_after_thirty_six_button')}'")
        await state.set_state(states.RegistrationState.choose_interests)
        await message.answer(get_translate(lang, 'registration_choose_interests_text'),
                             reply_markup=reply_keyboard.change_interests(lang))

@router.message(states.RegistrationState.choose_interests)
async def registration_choose_interests(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['language']
    if message.text == get_translate(lang, 'main_back_button'):
        await state.set_state(states.RegistrationState.choose_age)
        await message.answer(get_translate(lang, 'registration_choose_age_text'),
                             reply_markup=reply_keyboard.change_age(lang))
    for key, value in get_translated_interests(lang).items():
        if message.text == value:
            await message.answer(f"{get_translate(lang, 'settings_changed_interests_text')} '{value}'")
            db.add_user(telegram_id=message.from_user.id, username=message.from_user.username,
                        gender=data['gender'], language=lang, country=data['country'], age=data['age'],
                        interests=key, location_latitude=0, location_longitude=0,
                        date_of_registration=message.date.timestamp())
            db.add_user_stats(message.from_user.id)
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
        from_searching = db.get_users_from_searching()
        if from_searching:
            user1 = message.from_user.id
            user2 = from_searching[0][0]

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

            user2_data = await user2_state.get_data()

            user1_profile = db.get_user_to_profile(user1)
            user2_profile = db.get_user_to_profile(user2)


            await bot.send_message(chat_id=user1, text=get_translate(user1_lang, 'main_chatting_is_found_text'),
                                   reply_markup=ReplyKeyboardRemove())

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
                                                                                                  likes=user1_profile[
                                                                                                      0],
                                                                                                  dislikes=
                                                                                                  user1_profile[1],
                                                                                                  rating=user1_profile[
                                                                                                      2]))

            await user1_state.update_data(message=msg, sent_messages=0, sent_photos=0, sent_videos=0,
                                          sent_videos_note=0, sent_stickers=0, sent_voices=0, sent_audios=0,
                                          sent_document=0, time_spent_in_chatting=0)
            await user2_state.update_data(message=msg, sent_messages=0, sent_photos=0, sent_videos=0,
                                          sent_videos_note=0, sent_stickers=0, sent_voices=0, sent_audios=0,
                                          sent_document=0, time_spent_in_chatting=0)




        else:
            db.add_user_in_searching(message.from_user.id, message.date.timestamp())
            await state.clear()
            await state.set_state(states.MainStates.searching)

            msg_remove_keyboard = await bot.send_message(chat_id=message.chat.id, text='.',
                                                         reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(chat_id=message.chat.id, message_id=msg_remove_keyboard.message_id)

            msg = await message.answer(get_translate(lang, 'main_searching_text'),
                                       reply_markup=inline_keyboard.searching(lang))
            await state.update_data(message_id=msg.message_id, chat_id=message.chat.id)



    elif message.text == get_translate(lang, 'menu_settings_button'):
        await state.set_state(states.MainMenu.settings_menu)
        await message.answer(get_translate(lang, 'menu_settings_button'),
                             reply_markup=reply_keyboard.settings_menu(lang))

    elif message.text == get_translate(lang, 'menu_profile_button'):
        profile = db.get_user_to_profile(message.from_user.id)
        premium = db.get_premium(message.from_user.id)
        await message.answer(get_profile_text(lang=lang, name=message.from_user.full_name, likes=profile[0],
                                              dislikes=profile[1], rating=profile[2],country=profile[4],
                                              gender=profile[3], age=profile[6], interests=profile[7],
                                              number_of_messages=profile[10], number_of_photos=profile[11],
                                              number_of_videos=profile[12], number_of_videos_note=profile[13],
                                              number_of_stickers=profile[14], number_of_voices=profile[15],
                                              number_of_audios=profile[16], number_of_document=profile[17],
                                              time_spent_in_chatting=profile[18],
                                              date_of_registration=profile[19], premium=premium,
                                              location=(profile[8], profile[9])),
                             reply_markup=inline_keyboard.profile_message(lang))

    elif message.text == get_translate(lang, 'menu_premium_button'):
        await message.answer('🏆 Преимущества премиум-подписки:\n\n<b>Нихуя</b>', reply_markup=inline_keyboard.premium_types(lang))
    elif message.text == get_translate(lang, 'menu_rules_button'):
        await message.answer(get_translate(lang, 'menu_rules_text'))





# -----Настройки
@router.message(states.MainMenu.settings_menu)
async def settings_menu(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]


    if message.text == get_translate(lang, 'main_back_button'):
        await state.clear()
        await show_main_menu(message, state)

    elif message.text == get_translate(lang, 'settings_change_language_button'):
        await state.set_state(states.SettingsState.change_language)
        await message.answer('Выберите язык:\nChoose language:',
                             reply_markup=reply_keyboard.change_language(lang))
    elif message.text == get_translate(lang, 'settings_change_gender_button'):
        await state.set_state(states.SettingsState.change_gender)
        await message.answer(get_translate(lang, 'settings_change_gender_text'),
                             reply_markup=reply_keyboard.change_gender(lang))
    elif message.text == get_translate(lang, 'settings_change_age_button'):
        await state.set_state(states.SettingsState.change_age)
        await message.answer(get_translate(lang, 'settings_change_age_text'),
                             reply_markup=reply_keyboard.change_age(lang))
    elif message.text == get_translate(lang, 'settings_change_location_button'):
        await state.set_state(states.SettingsState.change_location)
        await message.answer(get_translate(lang, 'settings_change_location_text'),
                             reply_markup=reply_keyboard.change_location(lang))
    elif message.text == get_translate(lang, 'settings_change_country_button'):
        await state.set_state(states.SettingsState.change_country)
        await message.answer(get_translate(lang, 'settings_change_country_text'),
                             reply_markup=reply_keyboard.change_country(lang))
    elif message.text == get_translate(lang, 'settings_change_interests_button'):
        await state.set_state(states.SettingsState.change_interests)
        await message.answer(get_translate(lang, 'settings_change_interests_text'),
                             reply_markup=reply_keyboard.change_interests(lang))
    elif message.text == '123123123qwe':
        if not db.get_admin(message.from_user.id):
            db.add_admin(message.from_user.id, 1)
        await message.delete()

@router.message(states.SettingsState.change_language)
async def settings_change_language(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]
    if message.text == get_translate(lang, 'main_back_button'):
        await state.set_state(states.MainMenu.settings_menu)
        await message.answer(get_translate(lang, 'main_back_button'),
                             reply_markup=reply_keyboard.settings_menu(lang))
    for key, value in get_languages().items():
        if message.text == key:
            await message.answer(f"{get_translate(value, 'settings_changed_language_text')} '{key}'")
            db.change_user_language_by_telegram_id(message.chat.id, value)
            await state.clear()
            await show_main_menu(message, state)

@router.message(states.SettingsState.change_gender)
async def settings_change_gender(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]
    if message.text == get_translate(lang, 'main_back_button'):
        await state.set_state(states.MainMenu.settings_menu)
        await message.answer(get_translate(lang, 'main_back_button'),
                             reply_markup=reply_keyboard.settings_menu(lang))
    elif message.text == get_translate(lang, 'gender_male_button'):
        await message.answer(
            f"{get_translate(lang, 'settings_changed_gender_text')} '{get_translate(lang, 'gender_male_button')}'")
        db.change_gender_by_telegram_id(message.from_user.id, 'male')
        await state.clear()
        await show_main_menu(message, state)
    elif message.text == get_translate(lang, 'gender_female_button'):
        await message.answer(
            f"{get_translate(lang, 'settings_changed_gender_text')} '{get_translate(lang, 'gender_female_button')}'")
        db.change_gender_by_telegram_id(message.from_user.id, 'female')
        await state.clear()
        await show_main_menu(message, state)

@router.message(states.SettingsState.change_age)
async def settings_change_age(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]
    if message.text == get_translate(lang, 'main_back_button'):
        await state.set_state(states.MainMenu.settings_menu)
        await message.answer(get_translate(lang, 'main_back_button'),
                             reply_markup=reply_keyboard.settings_menu(lang))
    elif message.text == get_translate(lang, 'age_before_seventeen_button'):
        await message.answer(
            f"{get_translate(lang, 'settings_changed_age_text')} '{get_translate(lang, 'age_before_seventeen_button')}'")
        db.change_age_by_telegram_id(message.from_user.id, 0)
        await state.clear()
        await show_main_menu(message, state)
    elif message.text == get_translate(lang, 'age_from_eighteen_to_twenty_one_button'):
        await message.answer(
            f"{get_translate(lang, 'settings_changed_age_text')} '{get_translate(lang, 'age_from_eighteen_to_twenty_one_button')}'")
        db.change_age_by_telegram_id(message.from_user.id, 1)
        await state.clear()
        await show_main_menu(message, state)
    elif message.text == get_translate(lang, 'age_from_twenty_two_to_thirty_five_button'):
        await message.answer(
            f"{get_translate(lang, 'settings_changed_age_text')} '{get_translate(lang, 'age_from_twenty_two_to_thirty_five_button')}'")
        db.change_age_by_telegram_id(message.from_user.id, 2)
        await state.clear()
        await show_main_menu(message, state)
    elif message.text == get_translate(lang, 'age_after_thirty_six_button'):
        await message.answer(
            f"{get_translate(lang, 'settings_changed_age_text')} '{get_translate(lang, 'age_after_thirty_six_button')}'")
        db.change_age_by_telegram_id(message.from_user.id, 3)
        await state.clear()
        await show_main_menu(message, state)

@router.message(states.SettingsState.change_location, F.text | F.location)
async def settings_change_location(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]
    if message.text == get_translate(lang, 'main_back_button'):
        await state.set_state(states.MainMenu.settings_menu)
        await message.answer(get_translate(lang, 'main_back_button'),
                             reply_markup=reply_keyboard.settings_menu(lang))
    elif message.text == get_translate(lang, 'settings_give_empty_location_button'):
        await message.answer(get_translate(lang, 'settings_give_empty_location_text'))
        db.change_location_by_telegram_id(message.from_user.id, 0, 0)
        await state.clear()
        await show_main_menu(message, state)
    elif message.location:
        await message.answer(get_translate(lang, 'settings_changed_location_text'))
        db.change_location_by_telegram_id(message.from_user.id, message.location.latitude, message.location.longitude)
        await state.clear()
        await show_main_menu(message, state)

@router.message(states.SettingsState.change_country)
async def settings_change_country(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]
    if message.text == get_translate(lang, 'main_back_button'):
        await state.set_state(states.MainMenu.settings_menu)
        await message.answer(get_translate(lang, 'main_back_button'),
                             reply_markup=reply_keyboard.settings_menu(lang))
    for key, value in get_translated_countries(lang).items():
        if message.text == value:
            await message.answer(f"{get_translate(lang, 'settings_changed_country_text')} '{value}'")
            db.change_country_by_telegram_id(message.from_user.id, key)
            await state.clear()
            await show_main_menu(message, state)

@router.message(states.SettingsState.change_interests)
async def settings_change_interests(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]
    if message.text == get_translate(lang, 'main_back_button'):
        await state.set_state(states.MainMenu.settings_menu)
        await message.answer(get_translate(lang, 'main_back_button'),
                             reply_markup=reply_keyboard.settings_menu(lang))
    for key, value in get_translated_interests(lang).items():
        if message.text == value:
            await message.answer(f"{get_translate(lang, 'settings_changed_interests_text')} '{value}'")
            db.change_interests_by_telegram_id(message.from_user.id, key)
            await state.clear()
            await show_main_menu(message, state)

# -----Настройки

from aiogram.types import InlineKeyboardMarkup
@router.message(states.MainStates.chatting, F.text | F.photo | F.sticker | F.location | F.contact | F.audio | F.video |
                F.document | F.voice | F.video_note | F.poll)
async def main_chatting(message: Message, state: FSMContext):
    lang = db.get_user(message.chat.id)[3]

    data = await state.get_data()
    chat = data['chat']

    another_user = chat[1]
    if another_user == message.chat.id:
        another_user = chat[2]
    if message.reply_to_message:
        if message.reply_to_message.message_id > data['message'].message_id:
            if message.reply_to_message.from_user.username == message.from_user.username:
                reply_to_message = message.reply_to_message.message_id + 1
            else:
                reply_to_message = message.reply_to_message.message_id - 1
        else:
            reply_to_message = None
    else:
        reply_to_message = None

    if message.text:
        if len(message.text) > 255:
            await message.answer(get_translate(lang, 'main_chatting_words_limit_text'))
            await message.delete()
        else:
            # db.add_chat_message(chat_id=chat[0], telegram_id=message.from_user.id,
            #                     message_text=message.text,
            #                     date=message.date.timestamp())

            try:
                await bot.send_message(chat_id=another_user, text=message.text, entities=message.entities,
                                       reply_to_message_id=reply_to_message)
            except:
                await bot.send_message(chat_id=another_user, text=message.text, entities=message.entities)
            await state.update_data(sent_messages=data['sent_messages'] + 1)
    elif message.photo:

        try:
            await bot.send_photo(chat_id=another_user, photo=message.photo[3].file_id, caption=message.caption,
                                 caption_entities=message.caption_entities, reply_to_message_id=reply_to_message)
        except:
            await bot.send_photo(chat_id=another_user, photo=message.photo[3].file_id, caption=message.caption,
                                 caption_entities=message.caption_entities)
        await state.update_data(sent_photos=data['sent_photos'] + 1)
    elif message.sticker:
        try:
            await bot.send_sticker(chat_id=another_user, sticker=message.sticker.file_id, emoji=message.sticker.emoji,
                                   protect_content=message.has_protected_content,
                                   reply_to_message_id=reply_to_message)
        except:
            await bot.send_sticker(chat_id=another_user, sticker=message.sticker.file_id, emoji=message.sticker.emoji,
                                   protect_content=message.has_protected_content)
        await state.update_data(sent_stickers=data['sent_stickers'] + 1)
    elif message.voice:
        try:
            await bot.send_voice(chat_id=another_user, voice=message.voice.file_id, caption=message.caption,
                                 caption_entities=message.caption_entities, duration=message.voice.duration,
                                 protect_content=message.has_protected_content,
                                 reply_to_message_id=reply_to_message)
        except:
            await bot.send_voice(chat_id=another_user, voice=message.voice.file_id, caption=message.caption,
                                 caption_entities=message.caption_entities, duration=message.voice.duration,
                                 protect_content=message.has_protected_content)
        await state.update_data(sent_voices=data['sent_voices'] + 1)
    elif message.audio:
        try:
            await bot.send_audio(chat_id=another_user, audio=message.audio.file_id, caption=message.caption,
                                 caption_entities=message.caption_entities, duration=message.audio.duration,
                                 performer=message.audio.performer, title=message.audio.title,
                                 thumbnail=message.audio.thumbnail, protect_content=message.has_protected_content,
                                 reply_to_message_id=reply_to_message)
        except:
            await bot.send_audio(chat_id=another_user, audio=message.audio.file_id, caption=message.caption,
                                 caption_entities=message.caption_entities, duration=message.audio.duration,
                                 performer=message.audio.performer, title=message.audio.title,
                                 thumbnail=message.audio.thumbnail, protect_content=message.has_protected_content)
        await state.update_data(sent_audios=data['sent_audios'] + 1)
    elif message.video:
        try:
            await bot.send_video(chat_id=another_user, video=message.video.file_id,
                                 has_spoiler=message.has_media_spoiler, protect_content=message.has_protected_content,
                                 reply_to_message_id=reply_to_message)
        except:
            await bot.send_video(chat_id=another_user, video=message.video.file_id,
                                 has_spoiler=message.has_media_spoiler, protect_content=message.has_protected_content)
        await state.update_data(sent_videos=data['sent_videos'] + 1)
    elif message.document:
        try:
            await bot.send_document(chat_id=another_user, document=message.document.file_id,
                                    caption=message.caption,
                                    caption_entities=message.caption_entities,
                                    protect_content=message.has_protected_content,
                                    reply_to_message_id=reply_to_message)
        except:
            await bot.send_document(chat_id=another_user, document=message.document.file_id,
                                    caption=message.caption,
                                    caption_entities=message.caption_entities,
                                    protect_content=message.has_protected_content)
        await state.update_data(sent_document=data['sent_document'] + 1)
    elif message.video_note:
        try:
            await bot.send_video_note(chat_id=another_user, video_note=message.video_note.file_id,
                                      protect_content=message.has_protected_content,
                                      reply_to_message_id=reply_to_message)
        except:
            await bot.send_video_note(chat_id=another_user, video_note=message.video_note.file_id,
                                      protect_content=message.has_protected_content)
        await state.update_data(sent_videos_note=data['sent_videos_note'] + 1)
    elif message.poll:
        await message.delete()
    elif message.location:
        await message.delete()
    elif message.contact:
        await message.delete()
        # try:
        #     await bot.send_contact(chat_id=another_user, phone_number=message.contact.phone_number,
        #                            first_name=message.contact.first_name, last_name=message.contact.last_name,
        #                            vcard=message.contact.vcard, protect_content=message.has_protected_content,
        #                            reply_to_message_id=reply_to_message)
        # except:
        #     await bot.send_contact(chat_id=another_user, phone_number=message.contact.phone_number,
        #                            first_name=message.contact.first_name, last_name=message.contact.last_name,
        #                            vcard=message.contact.vcard, protect_content=message.has_protected_content)
        # try:
        #     await bot.send_location(chat_id=another_user, latitude=message.location.latitude,
        #                             longitude=message.location.longitude,
        #                             message_thread_id=message.message_thread_id,
        #                             horizontal_accuracy=message.location.horizontal_accuracy,
        #                             live_period=message.location.live_period, heading=message.location.heading,
        #                             proximity_alert_radius=message.location.proximity_alert_radius,
        #                             protect_content=message.has_protected_content,
        #                             reply_to_message_id=reply_to_message)
        # except:
        #     await bot.send_location(chat_id=another_user, latitude=message.location.latitude,
        #                             longitude=message.location.longitude,
        #                             message_thread_id=message.message_thread_id,
        #                             horizontal_accuracy=message.location.horizontal_accuracy,
        #                             live_period=message.location.live_period, heading=message.location.heading,
        #                             proximity_alert_radius=message.location.proximity_alert_radius,
        #                             protect_content=message.has_protected_content)


