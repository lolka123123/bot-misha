from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from data.loader import db
from data.translate import get_languages, get_translate, get_translated_countries, get_translated_interests
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class ReplyKeyboard:
    def choose_language(self):


        lst = []
        for button in get_languages().keys():
            lst.append(KeyboardButton(text=button))


        markup = ReplyKeyboardMarkup(keyboard=[lst], resize_keyboard=True)

        return markup




    def main_menu(self, lang):
        # markup = ReplyKeyboardMarkup(resize_keyboard=True)

        start = KeyboardButton(text=get_translate(lang, 'menu_start_button'))

        profile = KeyboardButton(text=get_translate(lang, 'menu_profile_button'))
        rules = KeyboardButton(text=get_translate(lang, 'menu_rules_button'))


        settings = KeyboardButton(text=get_translate(lang, 'menu_settings_button'))
        premium = KeyboardButton(text=get_translate(lang, 'menu_premium_button'))



        buttons = [[start], [profile, rules], [settings, premium]]

        markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

        return markup

    def settings_menu(self, lang):


        change_language = KeyboardButton(text=get_translate(lang, 'settings_change_language_button'))
        change_country = KeyboardButton(text=get_translate(lang, 'settings_change_country_button'))
        change_gender = KeyboardButton(text=get_translate(lang, 'settings_change_gender_button'))
        change_age = KeyboardButton(text=get_translate(lang, 'settings_change_age_button'))
        change_interests = KeyboardButton(text=get_translate(lang, 'settings_change_interests_button'))
        change_location = KeyboardButton(text=get_translate(lang, 'settings_change_location_button'))
        back = KeyboardButton(text=get_translate(lang, 'main_back_button'))

        buttons = [
            [change_language, change_country],
            [change_gender, change_age],
            [change_interests, change_location],
            [back]
        ]

        markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

        return markup

    def change_language(self, lang):


        lst = []
        for button in get_languages().keys():
            lst.append(KeyboardButton(text=button))

        back = KeyboardButton(text=get_translate(lang, 'main_back_button'))


        markup = ReplyKeyboardMarkup(keyboard=[lst, [back]], resize_keyboard=True)

        return markup

    def change_gender(self, lang):

        male = KeyboardButton(text=get_translate(lang, 'gender_male_button'))
        female = KeyboardButton(text=get_translate(lang, 'gender_female_button'))
        back = KeyboardButton(text=get_translate(lang, 'main_back_button'))

        lst = [[male, female],
               [back]]
        markup = ReplyKeyboardMarkup(keyboard=lst, resize_keyboard=True)

        return markup

    def change_age(self, lang):

        before_seventeen_button = KeyboardButton(text=get_translate(lang, 'age_before_seventeen_button'))
        from_eighteen_to_twenty_one_button = KeyboardButton(text=get_translate(lang, 'age_from_eighteen_to_twenty_one_button'))
        from_twenty_two_to_thirty_five_button = KeyboardButton(text=get_translate(lang, 'age_from_twenty_two_to_thirty_five_button'))
        after_thirty_six_button = KeyboardButton(text=get_translate(lang, 'age_after_thirty_six_button'))
        back = KeyboardButton(text=get_translate(lang, 'main_back_button'))

        lst = [[before_seventeen_button, from_eighteen_to_twenty_one_button],
               [from_twenty_two_to_thirty_five_button, after_thirty_six_button],
               [back]]
        markup = ReplyKeyboardMarkup(keyboard=lst, resize_keyboard=True)

        return markup

    def change_location(self, lang):
        give_location = KeyboardButton(text=get_translate(lang, 'settings_give_location_button'), request_location=True)
        give_empty_location = KeyboardButton(text=get_translate(lang, 'settings_give_empty_location_button'))
        back = KeyboardButton(text=get_translate(lang, 'main_back_button'))

        lst = [[give_location],
               [give_empty_location],
               [back]]
        markup = ReplyKeyboardMarkup(keyboard=lst, resize_keyboard=True)

        return markup

    def change_country(self, lang):
        builder = ReplyKeyboardBuilder()


        [builder.button(text=button) for button in get_translated_countries(lang).values()]

        back = KeyboardButton(text=get_translate(lang, 'main_back_button'))
        builder.adjust(3)
        builder.row(back)
        return builder.as_markup(resize_keyboard=True)

    def change_interests(self, lang):
        builder = ReplyKeyboardBuilder()

        [builder.button(text=button) for button in get_translated_interests(lang).values()]

        back = KeyboardButton(text=get_translate(lang, 'main_back_button'))
        builder.adjust(3)
        builder.row(back)
        return builder.as_markup(resize_keyboard=True)





        # lst = []
        # lst2 = []
        # count = 0
        # for button in get_translated_countries(lang).values():
        #     if count < 3:
        #         lst2.append(KeyboardButton(text=button))
        #         count += 1
        #     else:
        #         lst.append(lst2)
        #         lst2 = []
        #         lst2.append(KeyboardButton(text=button))
        #         count = 0
        #
        #
        # markup = ReplyKeyboardMarkup(keyboard=lst, resize_keyboard=True)
        # return markup


reply_keyboard = ReplyKeyboard()
