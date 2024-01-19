import os
import multiprocessing

from opentele.td import TDesktop
from opentele.api import CreateNewSession, UseCurrentSession
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

from main_bot.files import get_message
from main_bot.etc.functions import get_accounts


async def telegram_thread(group_name: str):
    '''Получение пользователей и запись в файл со всеми пользователями'''

    accounts = get_accounts()
    message = get_message(social='telegram')

    for account in accounts:
        try:
            tdata = os.path.join(os.path.abspath('input/telegram_accounts/' + account))
            exist=False
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

            async with client:
                participants = await client(GetParticipantsRequest(
                    channel=group_name,
                    filter=ChannelParticipantsSearch(''),
                    offset=0,
                    limit=100,
                    hash=0
                ))

                for user in participants.users:
                    try:
                        await client.send_message(user, message=message)
                    except Exception as _ex:
                        print(_ex)
                    finally:
                        await client.disconnect()
        except Exception as _ex:
            print(_ex)
            continue