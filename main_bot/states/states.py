from aiogram.fsm.state import StatesGroup, State


class GetGroup(StatesGroup):
    group = State()
    message = State()

