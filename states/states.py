from aiogram.dispatcher.filters.state import StatesGroup, State


class ByText(StatesGroup):
    guess_letters = State()
