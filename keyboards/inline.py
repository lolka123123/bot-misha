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

inline_keyboard = InlineKeyboard()