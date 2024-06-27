from aiogram.fsm.state import StatesGroup, State


class AuthUser(StatesGroup):
    user = State()
    password = State()


class CurrentSpam(StatesGroup):
    current_spam = State()

class TelegramSpamGroup(StatesGroup):
    telegram_group = State()
    account_count = State()
    message_count = State()

class AddAccounts(StatesGroup):
    add = State()