from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from .states.states import GetGroup
from .files import new_message, get_user_id

main_router = Router()


@main_router.message(CommandStart())
async def start_message(message: types.Message):
    await message.reply('Отправь ссылку на группу для получения пользователей, в таком виде "Группа (ссылка на группу)"')


@main_router.message(GetGroup.group, F.text.startswith('Гру'))
async def group(message: types.Message, state: FSMContext):
    try:
        await message.answer('Готово, напишите текст для пользователей, в таком виде "Сообщение (ваше сообщение)"!')
        await state.set_state(GetGroup.group)
        print(GetGroup.message)
    except Exception as _ex:
        print(_ex)
        await message.reply('Произошла какая то ошибка, обратитесь к разработчику :)')


@main_router.message(GetGroup.message, F.text.startswith('Соо'))
async def hello_message(message: types.Message):
