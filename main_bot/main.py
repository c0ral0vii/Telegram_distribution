from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext


from bots.telegram_message.main import telegram_thread
from .files import new_message


main_router = Router()


@main_router.message(CommandStart())
async def start_message(message: types.Message):
    '''/start'''

    await message.reply('Отправь ссылку на группу для получения пользователей, в таком виде "Группа (ссылка на группу)" или измени сообщение командой "Сообщение (ваше сообщение)"')


@main_router.message(F.text.startswith('Гру'))
async def group(message: types.Message):
    '''Рассылка для пользователей из группы'''

    try:
        await telegram_thread(group_name=message.text)
        await message.answer('Готово, напишите текст для пользователей, в таком виде "Сообщение (ваше сообщение)"!')
    except Exception as _ex:
        print(_ex)
        await message.reply('Произошла какая то ошибка, обратитесь к разработчику :)')


@main_router.message(F.text.startswith('Соо'))
async def change_message(message: types.Message):
    '''Изменение сообщения для рассылки'''
    try:
        new_message(message=message.text)
        await message.reply('Готово, сообщение изменилось')
    except Exception as _ex:
        print(_ex)