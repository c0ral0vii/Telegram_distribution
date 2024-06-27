from aiogram import BaseMiddleware, Bot
from aiogram.types import Message

from models.accounts import get_root_accounts


class AuthMiddleware(BaseMiddleware):
    def __init__(self):
        self.users_id = get_root_accounts()
        print(self.users_id)