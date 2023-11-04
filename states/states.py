# from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.fsm.state import State, StatesGroup


class States:
    class RegistrationState(StatesGroup):
        choose_language = State()
        choose_gender = State()

    class MainMenu(StatesGroup):
        main_menu = State()
        settings_menu = State()

    class SettingsChangeLanguage(StatesGroup):
        choose_language = State()

    class MainStates(StatesGroup):
        searching = State()
        chatting = State()


states = States()