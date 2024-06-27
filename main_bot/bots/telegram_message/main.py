import json
import random
import asyncio

import aiofiles
import numpy as np
import socks

from telethon import TelegramClient, events
from telethon.errors import PhoneNumberBannedError, UserDeactivatedBanError, \
    UserDeactivatedError, InviteHashExpiredError, FloodWaitError
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest

from main_bot.etc.functions import get_accounts, get_proxy
from main_bot.files import get_message
from models.accounts import get_accounts_db, change_status, add_users, get_users, add_history, add_account


class TClient:
    def __init__(self, account, message: str, users: list, count: int, group: str = None):
        self.account = account

        self.count = count
        self.users = users
        self.group = group
        self.message = message

    async def connect_(self):
        try:
            self.proxy = self.account.proxy
            self.client = TelegramClient(f'input\\telegram_accounts\\{self.account.phone}.session',
                                         api_id=6,
                                         api_hash=self.account.app_hash,
                                         device_model=self.account.device_model,
                                         app_version=self.account.app_version,
                                         system_version='4.16.30-vxCUSTOM',
                                         loop=asyncio.set_event_loop(asyncio.SelectorEventLoop()),
                                         proxy=(socks.SOCKS5, self.proxy[0], self.proxy[1], True, self.proxy[-2],
                                                self.proxy[-1]),
                                         )
            await self.client.connect()
            await self.client.get_entity('me')
        except Exception as e:
            if FileNotFoundError:
                print(e)
                return False
            if UserDeactivatedBanError or PhoneNumberBannedError:
                print(e)
                await change_status(True, phone=self.account.phone)

    async def disconnect(self):
        await self.client.disconnect()

    async def check_spam_block(self):
        # Сделать проверку на спам блок

        await self.client.send_message('@SpamBot', '/start')

        @self.client.on(events.NewMessage(chats='@SpamBot'))
        async def handler(event):
            await asyncio.sleep(2)
            print(f'Recieved message: {event.message.text}')

    async def connect_to_group(self):
        try:
            if '+' in self.group:
                await self.client(ImportChatInviteRequest(self.group.split('/')[-1].replace('+', '')))
                await asyncio.sleep(random.uniform(2, 4))
            else:
                await self.client(JoinChannelRequest(self.group))
                await asyncio.sleep(random.uniform(2, 4))

        except Exception as e:
            print(e)
            if e == UserDeactivatedError or e == PhoneNumberBannedError or e == UserDeactivatedBanError:
                await change_status(banned=True, phone=self.account.phone)
            if e == InviteHashExpiredError:
                return 'Срок действия ссылки для приглашения истёк либо вам нужно подождать пару минут'

    async def get_users(self):
        try:
            await self.client.connect()

            if '+' in self.group:
                await self.client(ImportChatInviteRequest(hash=self.group.split('/')[-1].replace('+', '')))
                users = await self.client.get_participants(self.group, aggressive=True)
                print(users)
                await add_users(users=users)

            else:
                entity = await self.client.get_entity(self.group)
                group_name = await self.client(JoinChannelRequest(entity))
                users = await self.client.get_participants(self.group, aggressive=True)
                print(len(users))
                await add_users(users=users)
            await self.disconnect()
        except UserDeactivatedBanError:
            await change_status(banned=True, phone=self.account.phone)

    async def send_messages(self):
        try:
            for user in self.users:
                if not user.username:
                    continue

                await asyncio.sleep(5)

                send_entity = await self.client.get_entity(user.username)
                await asyncio.sleep(5)

                query = await self.client.inline_query("@PostBot", "62ed0f7189df3")
                await asyncio.sleep(5)

                result = await query[0].click(send_entity)

                await add_history(from_account=self.account.phone, username=user.username,
                                  message=''.join(self.message))
                await asyncio.sleep(random.uniform(185, 200))
        except Exception as e:
            print(e)
            if e == UserDeactivatedError or e == PhoneNumberBannedError or e == UserDeactivatedBanError:
                print(e)

                await change_status(banned=True, phone=self.account.phone)
            if e == FloodWaitError:
                print(e)
        finally:
            await self.disconnect()

    async def main(self):
        if self.account.status != 'Banned':
            await self.connect_()
            await self.check_spam_block()
            # await self.send_messages()


async def start(user: int, count: int, group: str):
    '''Запуск спама'''

    message = get_message(social='telegram', user=user)
    accounts = await get_accounts_db()

    # await TClient(account=accounts[int(random.uniform(0, len(accounts)))], message=message, group=group, count=count, users=[]).main()

    await asyncio.sleep(random.uniform(2, 5))
    users = await get_users(count=count)
    chunks = [list(chunk) for chunk in np.array_split(users, len(accounts))]
    next_chunk = 0

    async with asyncio.TaskGroup() as task:
        for account in accounts:
            try:
                task.create_task(TClient(account=account, message=message, group=group, count=count,
                                         users=chunks[next_chunk]).main())
                next_chunk += 1
            except:
                continue


async def add_accounts():
    accounts = get_accounts()
    proxys = get_proxy()
    print(accounts)
    account_count = 0
    proxy_count = 0

    while account_count < len(accounts):
        if proxy_count < len(proxys):
            proxy_count -= 1
        try:
            async with aiofiles.open(fr'input\telegram_accounts\{accounts[account_count]}.json', 'r') as file:
                data = await file.read()
                js = json.loads(data)
        except FileNotFoundError:
            continue

        await add_account(app_hash=js['app_hash'], proxy=proxys[proxy_count], app_version=js['app_version'],
                          phone=js['phone'], device_model=js['device'])

        account_count += 1
        proxy_count += 1
    print('ready')
