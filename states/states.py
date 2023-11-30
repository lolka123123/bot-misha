# from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.fsm.state import State, StatesGroup


class States:
    class RegistrationState(StatesGroup):
        choose_language = State()
        choose_country = State()
        choose_gender = State()
        choose_age = State()
        choose_interests = State()

    class MainMenu(StatesGroup):
        main_menu = State()
        settings_menu = State()

    class SettingsState(StatesGroup):
        change_language = State()
        change_gender = State()
        change_age = State()
        change_location = State()
        change_country = State()
        change_interests = State()

    class MainStates(StatesGroup):
        searching = State()
        chatting = State()


states = States()