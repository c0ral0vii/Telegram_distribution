from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, KeyboardBuilder


async def start_spam():
    keyboard = KeyboardBuilder(button_type=KeyboardButton)

    keyboard.add(KeyboardButton(text='Начать рассылку'))

    return keyboard.as_markup()