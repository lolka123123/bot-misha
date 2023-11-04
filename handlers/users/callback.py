from data.loader import bot, dp, db
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from data.translate import get_translate

from states.states import states
from handlers.users.text_handlers import show_main_menu

from time import sleep

router = Router()

@router.callback_query(F.data == 'cansel')
async def main_searching_delete_message(call: CallbackQuery, state: FSMContext):
    lang = db.get_user(call.from_user.id)[3]
    if db.get_user_from_searching(call.from_user.id):
        data = await state.get_data()
        message_id = data['message_id']
        await bot.edit_message_text(text=get_translate(lang, 'main_searching_cansel_text'),
                                    chat_id=call.message.chat.id, message_id=message_id)
        db.remove_user_from_searching(call.message.chat.id)
        await state.clear()
        await show_main_menu(call.message, state)
    else:
        await call.message.delete()


# from handlers.users.text_handlers import show_main_menu
#
#
# @dp.callback_query(lambda call: call.data == 'cansel', state=states.MainMenu.main_menu)
# async def main_searching_delete_message(call: CallbackQuery):
#     await call.message.delete()
#
# @dp.callback_query(lambda call: call.data == 'cansel', state=states.MainStates.searching)
# async def main_searching(call: CallbackQuery, state: FSMContext):
#     lang = db.get_user(call.message.chat.id)[3]
#     async with state.proxy() as data:
#         message_id = data['message_id']
#         await bot.edit_message_text(text=get_translate(lang, 'main_searching_cansel_text'),
#                                     chat_id=call.message.chat.id, message_id=message_id)
#         db.remove_user_from_searching(call.message.chat.id)
#         await state.finish()
#         await show_main_menu(call.message)


