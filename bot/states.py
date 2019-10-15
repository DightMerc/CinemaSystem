from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    JustStarted = State()
    MainMenu = State()

    Cinema = State()
    Session = State()
    Cashback = State()
    Help = State()