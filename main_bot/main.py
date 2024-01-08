from aiogram import Router, F, types
from aiogram.filters import CommandStart


from .bots.telegram_message.main import telegram_thread
from .files import new_message_telegram, new_message_vk
from main_bot.etc.functions import get_accounts

main_router = Router()


@main_router.message(CommandStart())
async def start_message(message: types.Message):
    '''/start'''

    await message.reply('Отправь ссылку на группу для получения пользователей, в таком виде "Группа (ссылка на группу)" или измени сообщение командой "Сообщение (ваше сообщение)"')


@main_router.message(F.text.startswith('Гру'))
async def group(message: types.Message):
    '''Рассылка для пользователей из группы'''

    try:
        accounts = get_accounts()
        if len(accounts) == 0:
            await message.answer('В данный момент аккаунтов telegram - 0')
        else:
            await telegram_thread(group_name=message.text)
            await message.answer('Готово, напишите текст для пользователей, в таком виде "Сообщение (ваше сообщение)"!')
    except Exception as _ex:
        print(_ex)
        await message.reply('Произошла какая то ошибка, обратитесь к разработчику :)')


@main_router.message(F.text.startswith('Соо'))
async def change_message(message: types.Message):
    '''Изменение сообщения для рассылки'''

    try:
        new_message_telegram(message=message.text)
        await message.reply('Готово, сообщение изменилось')
    except Exception as _ex:
        print(_ex)
        await message.reply('Произошла какая то ошибка, обратитесь к разработчику :)')


@main_router.message(F.text.startswith('VK'))
async def vk_group(message: types.Message):
    '''Получение группы в вк'''

    ...


@main_router.message(F.text.startswith('VK'))
async def change_message_vk(message: types.Message):
    '''Изменение сообщения в вк'''

    try:
        new_message_telegram(message=message.text)
        await message.reply('Готово, сообщение изменилось')
    except Exception as _ex:
        print(_ex)
        await message.reply('Произошла какая то ошибка, обратитесь к разработчику :)')
