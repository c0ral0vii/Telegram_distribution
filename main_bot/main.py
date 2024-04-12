import os

from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

from .files import new_message, create_user


main_router = Router()


@main_router.message(CommandStart())
async def start_message(message: types.Message):
    '''Начальная команда - /start '''

    create_user(user=message.from_user.id)
    await message.reply('Отправь ссылку на группу для получения пользователей, в таком виде "Группа (ссылка на группу)" или измени сообщение командой "Сообщение:(ваше сообщение)"')


@main_router.message(F.text.startswith('Гру'))
async def group(message: types.Message):
    '''Рассылка для пользователей из группы'''

    accounts = os.listdir(os.path.abspath('input/telegram_accounts'))

    if len(accounts) == 0:
        await message.answer('В данный момент аккаунтов telegram - 0')
    else:
        await message.reply('Спам начинается...')
        count = message.text.split(' ')[-1]
        users = await start(user=message.from_user.id, count=count)
        await message.reply(f'Готово, {users}/{count}')
    


@main_router.message(F.text.startswith('Соо'))
async def change_message(message: types.Message):
    '''Изменение сообщения для рассылки'''

    try:
        new_message(message=message.text, social='telegram', user=message.from_user.id)
        await message.reply('Готово, сообщение изменилось')
    except Exception as _ex:
        print(_ex)
        await message.reply('Произошла какая то ошибка, обратитесь к разработчику :)')


@main_router.message(F.text.startswith('Стат'))
async def stats(message: types.Message):
    await message.reply('Идёт проверка аккаунтов...')
    accounts = check_accounts()
    await message.reply(f'Незабаненых телеграмм аккаунтов - {accounts[0]}/{accounts[1]}')


# @main_router.message(F.text.startswith('VK гру'))
# async def vk_group(message: types.Message):
#     '''Получение группы в вк'''

#     try:
#         accounts = os.listdir(os.path.abspath('input/telegram_accounts'))
#         if len(accounts) == 0:
#             await message.answer('В данный момент аккаунтов VK - 0')
#         else:
#             await telegram_thread(group_name=message.text.strip())
#             await message.answer('Готово, начинается рассылка')
#     except Exception as _ex:
#         print(_ex)
#         await message.reply('Произошла какая то ошибка, обратитесь к разработчику :)')


# @main_router.message(F.text.startswith('VK соо'))
# async def change_message_vk(message: types.Message):
#     '''Изменение сообщения в вк'''

#     try:
#         new_message(message=message.text, social='vk')
#         await message.reply('Готово, сообщение изменилось')
#     except Exception as _ex:
#         print(_ex)
#         await message.reply('Произошла какая то ошибка, обратитесь к разработчику :)')
