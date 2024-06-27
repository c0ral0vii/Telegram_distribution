import os

from aiogram import Router, F, types
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from main_bot.keyboards.keyboards import telegram_keyboard, current_spam_keyboard
from config.config import ADMIN_PASSWORD
from main_bot.fsm import AuthUser, CurrentSpam
from models.accounts import create_auth_user, check_account
from main_bot.middlewares.middleware import AuthMiddleware


main_router = Router()

@main_router.message(CommandStart(), StateFilter(None))
async def start_message(message: types.Message, state: FSMContext):
    '''Начальная команда - /start '''

    if not await check_account(message.from_user.id):
        await state.set_state(AuthUser.password)
        await message.reply('Отправь пароль для входа в систему...')
    else:
        await state.set_state(CurrentSpam.current_spam)
        await message.answer('Выберите спам:', reply_markup=await current_spam_keyboard())

@main_router.message(F.text, AuthUser.password)
async def login(message: types.Message, state: FSMContext):
    '''Вход'''

    if message.text == ADMIN_PASSWORD:

        await state.clear()

        await create_auth_user(user_id=message.from_user.id)
        await message.answer('Вы ввели правильный пароль')
        await state.set_state(CurrentSpam.current_spam)
        await message.answer('Выберите спам:', reply_markup=await current_spam_keyboard())
    else:
        await state.set_state(AuthUser.password)
        await message.answer('Вы ввели неправильный пароль')


@main_router.callback_query(F.data == 'telegram_spam', CurrentSpam.current_spam)
async def current_spam(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f'Спам был выбран - 👑TG👑', reply_markup=await telegram_keyboard())

@main_router.message(F.text == 'Изменить спам', CurrentSpam.current_spam)
async def change_spam(message: types.Message, state: FSMContext):
    '''Выбор спама'''

    await state.set_state(CurrentSpam.current_spam)
    await message.answer('Выберите спам:', reply_markup=await current_spam_keyboard())


@main_router.message(F.text == '📉Статистика📉', CurrentSpam.current_spam)
async def telegram_stats(message: types.Message, state: FSMContext):
    '''Статистика'''

    await message.answer('🔴Список аккаунтов пуст🔴')


@main_router.message(F.text == '👆Начать спам👆', CurrentSpam.current_spam)
async def start_spam(message: types.Message, state: FSMContext):
    '''Запуск спама'''

    await message.answer('🔴Отсутствуют аккаунты, невозможно запустить спам..🔴')


@main_router.message(F.text == 'Текущий спам', CurrentSpam.current_spam)
async def check_spam(message: types.Message, state: FSMContext):
    '''Статистика запущеного спама'''

    await message.answer(f'🔴В данный момент ни один спам не запущен..🔴')