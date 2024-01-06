import asyncio
import os
import aiohttp

from opentele.td import TDesktop
from opentele.api import API, CreateNewSession, UseCurrentSession
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

from main_bot.etc.functions import get_accounts




async def telegram_thread():
    '''Получение пользователей и запись в файл со вссеми пользователями'''

    accounts = get_accounts()

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        for account in accounts:
            try:
                tdata = os.path.join(os.path.abspath('input/telegram_accounts/' + account))
                tdesk = TDesktop(tdata)

                for file in os.listdir(os.path.abspath(tdata)):
                    if file.endswith(".session"):
                        exist = True
                if exist is True:
                    tdesk = TDesktop(tdata)
                    client = await tdesk.ToTelethon(session=f"{tdata}.session", flag=UseCurrentSession)
                else:
                    tdesk = TDesktop(tdata)
                    client = await tdesk.ToTelethon(session=f"{tdata}.session", flag=CreateNewSession)
                await client.connect()
                await client.PrintSessions()
            except Exception as _ex:
                print(_ex)

asyncio.run(telegram_thread())


