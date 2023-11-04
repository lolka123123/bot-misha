LANGUAGES = {
    'ru': {
        'language': 'Русский',

        'admin_no_access': '<b>У вас нет доступа к этой комманде</b>',

        'registration_choose_language': 'Выберите язык:',
        'registration_choose_gender_text': 'Укажите ваш пол:',

        'gender_male_button': '♂️ Мужской',
        'gender_female_button': '♀️ Женский',
        'gender_unknown_button': 'Не указан',

        'menu_start_button': '🔎 Начать поиск',
        'menu_settings_button': '⚙ Настройки',
        'menu_info_button': 'О боте',
        'menu_show_text': 'Halo',

        'menu_info_text': 'Какой-то текст',

        'main_back_button': '⬅ Назад',

        'settings_change_language_button': 'Сменить язык',

        'main_searching_text': '<b>идет поиск...</b>',
        'main_searching_cansel_button': 'Отмена',
        'main_searching_cansel_text': '<b>поиск отменен</b>',

        'main_chatting_is_found_text': 'собеседник найден\nЧтоб закончить разговор /stop',
        'main_chatting_words_limit_text': '<b>текст не может привышать 255 символов</b>',
        'main_chatting_finished_text': '<b>разговор окончен</b>',

    },






}



def get_translate(lang, text):
    try:
        lang_key = LANGUAGES[lang][text]
    except:
        lang_key = LANGUAGES[list(LANGUAGES.keys())[0]][text]
    return lang_key




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



# def get_languages():
#     dict = {}
#     for key, value in LANGUAGES.items():
#         dict[value['language']] = key
#     return dict
#
# print(get_languages())

