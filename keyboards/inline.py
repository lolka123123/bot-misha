from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.translate import get_translate
from data.loader import db


class InlineKeyboard:
    def searching(self, lang):

        cansel = InlineKeyboardButton(text=get_translate(lang, 'main_searching_cansel_button'), callback_data='cansel')

        buttons = [
            [cansel]
        ]

        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        return markup

    def close_message(self, lang):
        close = InlineKeyboardButton(text=get_translate(lang, 'close_message'), callback_data='close_message')
        buttons = [
            [close]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        return markup

    def profile_message(self, lang):
        settings = InlineKeyboardButton(text=get_translate(lang, 'menu_settings_button'), callback_data='settings')
        close = InlineKeyboardButton(text=get_translate(lang, 'close_message'), callback_data='close_message')
        buttons = [
            [settings],
            [close]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        return markup

    def likes(self, telegram_id):
        like = InlineKeyboardButton(text='👍', callback_data=f'like_{telegram_id}')
        dislike = InlineKeyboardButton(text='👎', callback_data=f'dislike_{telegram_id}')

        buttons = [
            [like, dislike]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        return markup

    def premium_types(self, lang):
        first = InlineKeyboardButton(text='1 день / 1.000.000 денег', callback_data=f'premium_first')
        close = InlineKeyboardButton(text=get_translate(lang, 'close_message'), callback_data='close_message')
        buttons = [
            [first],
            [close]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        return markup

    def premium_payment(self, lang, id):
        # url = InlineKeyboardButton(text='Перейти к оплате', url=f'{PENDING_URL}{id}/')
        url = InlineKeyboardButton(text='Перейти к оплате', url=f'https://anonimchatbot.uz/')
        check = InlineKeyboardButton(text='✅ Подтвердить', callback_data=f'payment_{id}')
        buttons = [
            [url],
            [check],
        ]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        return markup

inline_keyboard = InlineKeyboard()