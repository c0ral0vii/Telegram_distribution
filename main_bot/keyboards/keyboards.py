from aiogram.utils.keyboard import KeyboardButton, InlineKeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardButton

async def current_spam_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='TG', callback_data='telegram_spam'),
            InlineKeyboardButton(text='VK', callback_data='vk_spam'),
            InlineKeyboardButton(text='OK', callback_data='ok_spam'),
            InlineKeyboardButton(text='INSTA', callback_data='instagram_spam'),
    )

    return builder.as_markup()


async def telegram_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='📉Статистика📉'))
    builder.add(KeyboardButton(text='👆Начать спам👆'))
    builder.add(KeyboardButton(text='Текущий спам'))
    builder.add(KeyboardButton(text='Изменить спам'))
    builder.add(KeyboardButton(text='Добавить аккаунты'))

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)