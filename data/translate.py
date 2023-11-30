LANGUAGES = {
    'ru': {
        'language': 'Русский',

        'admin_no_access': '<b>У вас нет доступа к этой комманде</b>',

        'registration_choose_language': '📕 Выберите язык:',
        'registration_choose_country_text': '🌍 Укажите страну:',
        'registration_choose_gender_text': '👫 Укажите ваш пол:',
        'registration_choose_age_text': '📅 Укажите ваш возраст:',
        'registration_choose_interests_text': '🎯 Укажите вашы интересы:',

        'gender_male_button': '♂️ Мужской',
        'gender_female_button': '♀️ Женский',
        'gender_unknown_button': 'Не указан',

        'close_message': '❌ Закрыть',

        'age_before_seventeen_button': 'До 17 лет',
        'age_from_eighteen_to_twenty_one_button': 'От 18 до 21 года',
        'age_from_twenty_two_to_thirty_five_button': 'От 22 до 35 лет',
        'age_after_thirty_six_button': 'Более 35 лет',

        'menu_start_button': '🔎 Начать поиск',
        'menu_profile_button': '👤 Профиль',
        'menu_rules_button': '📖 Правила',
        'menu_premium_button': '🏆 Премиум',
        'menu_settings_button': '⚙ Настройки',

        'menu_show_text': 'Halo',

        'menu_rules_text': 'Какой-то текст',

        'main_back_button': '⬅ Назад',

        'settings_change_language_button': '📕 Язык',
        'settings_change_language_text': '📕 Сменить свой язык',
        'settings_changed_language_text': '📕 <b>Язык установлен на:</b>',

        'settings_change_country_button': '🌍 Страна',
        'settings_change_country_text': '🌍 Установить страну',
        'settings_changed_country_text': '🌍 <b>Страна установлена на:</b>',

        'settings_change_gender_button': '👫 Пол',
        'settings_change_gender_text': '👫 Установить свой пол',
        'settings_changed_gender_text': '👫 <b>Пол установлен на:</b>',

        'settings_change_age_button': '📅 Возраст',
        'settings_change_age_text': '📅 Установить свой возраст',
        'settings_changed_age_text': '📅 <b>Bозраст установлен на:</b>',

        'settings_change_interests_button': '🎯 Интересы',
        'settings_change_interests_text': '🎯 Установить свою интересы',
        'settings_changed_interests_text': '🎯 <b>Интерес установлен на:</b>',

        'settings_change_location_button': '📍 Расстояние',
        'settings_change_location_text': '📍 Установить свою локацию',
        'settings_give_location_button': '📍 Отправить локацию',
        'settings_give_empty_location_button': 'Не указывать',
        'settings_give_empty_location_text': '📍 Локация не указано',
        'settings_changed_location_text': '📍 <b>Локация установлена</b>',

        'main_searching_text': '<b>идет поиск...</b>',
        'main_searching_cansel_button': 'Отмена',
        'main_searching_cansel_text': '<b>поиск отменен</b>',

        'main_chatting_is_found_text': 'собеседник найден\nЧтоб закончить разговор /stop',
        'main_chatting_words_limit_text': '<b>текст не может привышать 255 символов</b>',
        'main_chatting_finished_text': '<b>разговор окончен</b>',
        'main_chatting_time_text': '🕑 <b>Вы общались:</b>',
        'main_chatting_likes_text': '💡 <b>Поставьте оценку собеседнику, которая будет влиять на его рейтинг.</b>',
        'main_chatting_liked_text': '<b>Отзыв отправлен</b>',


        'profile_name': 'Имя аккаунта:',
        'profile_likes': 'Лайки:',
        'profile_rating': '🥇 Рейтинг:',
        'profile_language': '📕 Ваш язык:',
        'profile_country': '🌍 Ваша страна:',
        'profile_gender': '👫 Ваш пол:',
        'profile_age': '📅 Ваш возраст:',
        'profile_interests': '🎯 Вашы интересы:',
        'profile_messages': '✉ Количество сообщений:',
        'profile_photos': '🖼 Количество фото:',
        'profile_videos': '🎞 Количество видео:',
        'profile_videos_note': '🔮 Количество видео в кружочкe:',
        'profile_stickers': '😁 Количество стикеров:',
        'profile_voices': '🎤 Количество голосовых сообщений:',
        'profile_audios': '🎵 Количество аудио:',
        'profile_document': '📄 Количество файлов:',
        'profile_time_spent_in_chatting': '⌚ Время проведенное в чате:',
        'profile_date_of_registration': '⌛ Дата регестрации:',
        'profile_location': '📍 Локация:',
        'profile_has_location': 'Указанно',
        'profile_hasnt_location': 'Не указанно',
        'profile_premium': '🏆 Премиум статус:',
        'profile_has_premium': 'До',
        'profile_hasnt_premium': 'Нет премиума',
        'profile_premium_stats': 'Статистика собеседника',




        'country_uzbekistan': 'Узбекистан',

        'interest_communication': 'Общение',
    },


}


from data.data import COUNTRIES, INTERESTS
from data.config import show_time
from datetime import datetime

def get_translate(lang, text):
    try:
        lang_key = LANGUAGES[lang][text]
    except:
        lang_key = LANGUAGES[list(LANGUAGES.keys())[0]][text]
    return lang_key

def get_translated_countries(lang):
    dct = {}
    for country in COUNTRIES:
        try:
            translated_country = get_translate(lang, f'country_{country}')
        except:
            translated_country = country
        dct[country] = translated_country
    return dct

def get_translated_interests(lang):
    dct = {}
    for interest in INTERESTS:
        try:
            translated_interest = get_translate(lang, f'interest_{interest}')
        except:
            translated_interest = interest
        dct[interest] = translated_interest
    return dct

def get_languages():
    dct = {}
    lst = []
    num = 0
    for key, value in LANGUAGES.items():
        try:
            if value['language'] in lst:
                dct[str(num)] = key
                num += 1
            else:
                dct[value['language']] = key
                lst.append(value['language'])
        except:
            dct[key] = key

    return dct


def get_profile_text(lang, name, likes, dislikes, rating, country, gender, age, interests,
                     number_of_messages, number_of_photos, number_of_videos, number_of_videos_note,
                     number_of_stickers, number_of_voices, number_of_audios, number_of_document,
                     time_spent_in_chatting, date_of_registration, premium, location):
    try:
        language = LANGUAGES[lang]['language']
    except:
        language = lang

    for key, value in get_translated_countries(lang).items():
        if country == key:
            country = value
            break

    for key, value in get_translated_interests(lang).items():
        if interests == key:
            interests = value
            break

    if gender == 'male':
        gender = get_translate(lang, 'gender_male_button')
    elif gender == 'female':
        gender = get_translate(lang, 'gender_female_button')

    if age == 0:
        age = get_translate(lang, 'age_before_seventeen_button')
    elif age == 1:
        age = get_translate(lang, 'age_from_eighteen_to_twenty_one_button')
    elif age == 2:
        age = get_translate(lang, 'age_from_twenty_two_to_thirty_five_button')
    elif age == 3:
        age = get_translate(lang, 'age_after_thirty_six_button')

    if premium:
        premium = f"{get_translate(lang, 'profile_has_premium')} ({datetime.fromtimestamp(premium[2]).strftime('%Y-%m-%d %H:%M:%S')})"
    else:
        premium = get_translate(lang, 'profile_hasnt_premium')

    if location[0] == 0 and location[1] == 0:
        location = get_translate(lang, 'profile_hasnt_location')
    else:
        location = get_translate(lang, 'profile_has_location')


    return f"""<b>{get_translate(lang, 'profile_name')}</b> {name}

<b>{get_translate(lang, 'profile_likes')}</b> (👍{likes}/👎{dislikes})
<b>{get_translate(lang, 'profile_rating')}</b> {rating}

<b>{get_translate(lang, 'profile_language')}</b> {language}
<b>{get_translate(lang, 'profile_country')}</b> {country}
<b>{get_translate(lang, 'profile_gender')}</b> {gender}
<b>{get_translate(lang, 'profile_age')}</b> {age}
<b>{get_translate(lang, 'profile_interests')}</b> {interests}

<b>{get_translate(lang, 'profile_premium')}</b> {premium}

<b>{get_translate(lang, 'profile_messages')}</b> {number_of_messages}
<b>{get_translate(lang, 'profile_photos')}</b> {number_of_photos}
<b>{get_translate(lang, 'profile_videos')}</b> {number_of_videos}
<b>{get_translate(lang, 'profile_videos_note')}</b> {number_of_videos_note}
<b>{get_translate(lang, 'profile_stickers')}</b> {number_of_stickers}
<b>{get_translate(lang, 'profile_voices')}</b> {number_of_voices}
<b>{get_translate(lang, 'profile_audios')}</b> {number_of_audios}
<b>{get_translate(lang, 'profile_document')}</b> {number_of_document}

<b>{get_translate(lang, 'profile_location')}</b> {location}

<b>{get_translate(lang, 'profile_time_spent_in_chatting')}</b> {show_time(time_spent_in_chatting)}
<b>{get_translate(lang, 'profile_date_of_registration')}</b> {datetime.fromtimestamp(date_of_registration).strftime('%Y-%m-%d %H:%M:%S')}
"""


def get_profile_to_premium_text(lang, likes, dislikes, rating, country, gender, age, interests, language):
    try:
        language = LANGUAGES[language]['language']
    except:
        language = language

    for key, value in get_translated_countries(lang).items():
        if country == key:
            country = value
            break

    for key, value in get_translated_interests(lang).items():
        if interests == key:
            interests = value
            break

    if gender == 'male':
        gender = get_translate(lang, 'gender_male_button')
    elif gender == 'female':
        gender = get_translate(lang, 'gender_female_button')

    if age == 0:
        age = get_translate(lang, 'age_before_seventeen_button')
    elif age == 1:
        age = get_translate(lang, 'age_from_eighteen_to_twenty_one_button')
    elif age == 2:
        age = get_translate(lang, 'age_from_twenty_two_to_thirty_five_button')
    elif age == 3:
        age = get_translate(lang, 'age_after_thirty_six_button')



    return f"""<b>{get_translate(lang, 'profile_premium_stats')}</b>
    
<b>{get_translate(lang, 'profile_likes')}</b> (👍{likes}/👎{dislikes})
<b>{get_translate(lang, 'profile_rating')}</b> {rating}

<b>{get_translate(lang, 'settings_change_language_button')}:</b> {language}
<b>{get_translate(lang, 'settings_change_country_button')}:</b> {country}
<b>{get_translate(lang, 'settings_change_gender_button')}:</b> {gender}
<b>{get_translate(lang, 'settings_change_age_button')}:</b> {age}
<b>{get_translate(lang, 'settings_change_interests_button')}:</b> {interests}
"""


def get_profile_without_premium_text(lang, likes, dislikes, rating):
    return f"""<b>{get_translate(lang, 'profile_premium_stats')}</b>

<b>{get_translate(lang, 'profile_likes')}</b> (👍{likes}/👎{dislikes})
<b>{get_translate(lang, 'profile_rating')}</b> {rating}
"""
