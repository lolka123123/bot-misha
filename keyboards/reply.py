from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from data.loader import db
from data.translate import get_languages, get_translate


class ReplyKeyboard:
    def choose_language(self):


        lst = []
        for button in get_languages().keys():
            lst.append(KeyboardButton(text=button))


        markup = ReplyKeyboardMarkup(keyboard=[lst], resize_keyboard=True)

        return markup


    def choose_gender(self, lang):

        male = KeyboardButton(text=get_translate(lang, 'gender_male_button'))
        female = KeyboardButton(text=get_translate(lang, 'gender_female_button'))

        lst = [male, female]
        markup = ReplyKeyboardMarkup(keyboard=[lst], resize_keyboard=True)

        return markup

    def main_menu(self, lang):
        # markup = ReplyKeyboardMarkup(resize_keyboard=True)

        start = KeyboardButton(text=get_translate(lang, 'menu_start_button'))
        settings = KeyboardButton(text=get_translate(lang, 'menu_settings_button'))
        info = KeyboardButton(text=get_translate(lang, 'menu_info_button'))

        buttons = [[start], [settings], [info]]

        markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

        return markup

    def settings_menu(self, lang):


        change_language = KeyboardButton(text=get_translate(lang, 'settings_change_language_button'))
        back = KeyboardButton(text=get_translate(lang, 'main_back_button'))

        buttons = [[change_language], [back]]

        markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

        return markup

reply_keyboard = ReplyKeyboard()
