import json
import os
import shutil
import asyncio
import aiofiles
import time
import socks

from telethon.sessions import StringSession
from telethon import TelegramClient, connection
from telethon.errors import PhoneNumberBannedError, ChannelBannedError, UserDeactivatedBanError

from main_bot.files import get_message
from main_bot.etc.functions import get_accounts, get_proxy


async def telegram_thread(users: list, account: str, message: str):
    '''Создание ядра с телеграмм аккаунтом'''

    ...


async def check_accounts() -> list:
    '''Получение всех аккаунтов'''

    accounts = get_accounts()
    proxys = get_proxy()
    print(proxys)
    already_accs = []
    banned_accounts = []

    for account in accounts:
        for proxy in proxys:
            async with aiofiles.open(f'../../../input/telegram_accounts/{account}.json', 'r') as file:
                data = await file.read()
                js = json.loads(data)
                print(js)

                client = TelegramClient(f'../../../input/telegram_accounts/{account}.session',
                                        api_id=js["app_id"],
                                        api_hash=js["app_hash"],
                                        app_version=js['app_version'],
                                        device_model=js['device'],
                                        system_version=js['sdk'],
                                        proxy=(socks.SOCKS5, f'{proxy}', 50101, True, 'demidovicpav', '7afed7819af815908dc1715aa'),
                                        )

                try:
                    await client.connect()
                    time.sleep(5)
                    if client.is_user_authorized():
                        time.sleep(3)
                        await client.send_message('@c0ral0vii', 'hi, bro, this is a test message ')
                        time.sleep(10)
                        client.disconnect()

                except UserDeactivatedBanError:
                    shutil.move(f'../../../input/telegram_accounts/{account}.session',
                                f'../../../input/telegram_accounts/banned/{account}.session')
                    shutil.move(f'../../../input/telegram_accounts/{account}.json',
                                f'../../../input/telegram_accounts/banned/{account}.json')
                    banned_accounts.append(account)
                time.sleep(10)

asyncio.run(check_accounts())
async def start(user: int, count: int):
    '''Запуск спама'''

    accounts = check_accounts()
    message = get_message(social='telegram', user=user)

    for account in accounts:
        ...

    return