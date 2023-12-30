from aiogram import Router, F, Dispatcher, types
from aiogram.filters import CommandStart

from .bots.telegram_message.main import get_users, send_message
from .files import new_message, clear_user_id

main_router = Router()


@main_router.message(CommandStart())
async def start_message(message: types.Message):
    await message.reply('Отправь ссылку на группу для получения пользователей')


@main_router.message()
async def hello(message: types.Message):
    await message.reply('Идёт обработка...')
    users = await get_users(group_username=message.text)

