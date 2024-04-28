import json
import random
import asyncio

import aiofiles
import numpy as np
import socks

from telethon import TelegramClient
from telethon.errors import PhoneNumberBannedError, ChannelBannedError, UserDeactivatedBanError, \
AuthKeyUnregisteredError, UserDeactivatedError, InviteHashExpiredError, FloodWaitError, InputUserDeactivatedError
from telethon.tl.functions.messages import ImportChatInviteRequest, CheckChatInviteRequest, SendInlineBotResultRequest
from telethon.tl.functions.channels import JoinChannelRequest

from main_bot.etc.functions import get_accounts, get_proxy
from main_bot.files import get_message
from services.accounts import get_accounts_db, change_status, add_users, get_users, add_history, add_account, \
    delete_users, delete_history


class TClient:
    def __init__(self, account, group: str, message: str, count: int, users: list):
        self.account = account

        self.count = count
        self.users = users
        self.group = group
        self.message = message

    async def connect(self):
        try:
            self.client = TelegramClient(f'input/telegram_accounts/{self.account.phone}.session',
                                        api_id=6,
                                        api_hash=self.account.app_hash,
                                        device_model=self.account.device_model,
                                        app_version=self.account.app_version,
                                        system_version='4.16.30-vxCUSTOM',
                                        loop=asyncio.set_event_loop(asyncio.SelectorEventLoop()),
                                        )
            await self.client.connect()
            await self.client.get_entity('me')
        except FileNotFoundError:
            return False

    async def disconnect(self):
        await self.client.disconnect()

    async def check_spam_ban(self):
        checker_bot = await self.client.get_entity('@spambot')
        await self.client.send_message(checker_bot, '/start')
        messages = await self.client.get_drafts(entity=checker_bot)
        print(messages)

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

    async def send_messages(self):
            for user in self.users:
                try:

                    if not user.username:
                        continue

                    await asyncio.sleep(random.uniform(2,5))
                    entity = await self.client.get_entity(int(user.username))
                    await asyncio.sleep(random.uniform(15,30))
                    query = await self.client.inline_query('@PostBot', query=self.message[-1], offset='0')
                    await asyncio.sleep(random.uniform(2,4))
                    result = await query[0].click(entity)

                    await add_history(from_account=self.account.phone, username=user.username)
                    await asyncio.sleep(random.uniform(185, 420))
                except Exception as e:
                    print(e)
                    if e == UserDeactivatedError or e == PhoneNumberBannedError or e == UserDeactivatedBanError or e == InputUserDeactivatedError:
                        await change_status(banned=True, phone=self.account.phone)

                    if e == FloodWaitError:
                        await asyncio.sleep(60)

                        await asyncio.sleep(random.uniform(2, 5))
                        entity = await self.client.get_entity(user.username)

                        await asyncio.sleep(random.uniform(15, 30))
                        query = await self.client.inline_query('@PostBot', query=self.message[-1], offset='0')
                        await asyncio.sleep(random.uniform(2, 4))
                        result = await query[0].click(entity)

                    if e == SendInlineBotResultRequest:
                        print(self.account.phone, 'flood')
                        await asyncio.sleep(60)

                        await asyncio.sleep(random.uniform(2, 5))
                        entity = await self.client.get_entity(int(user.username))

                        await asyncio.sleep(random.uniform(15, 30))
                        query = await self.client.inline_query('@PostBot', query=self.message[-1], offset='0')
                        await asyncio.sleep(random.uniform(2, 4))
                        result = await query[0].click(entity)

            await self.disconnect()

    async def get_users(self):
        await self.connect()

        if '+' in self.group:
            await self.client(ImportChatInviteRequest(hash=self.group.split('/')[-1].replace('+', '')))
            users = await self.client.get_participants(self.group, aggressive=True)
            print(len(users))
            if len(users) < 20:
                messages = await self.client.get_messages(entity=self.group.split('/')[-1], limit=5000)
                for message in messages:
                    if message.sender_id:
                        await add_users(users=message.sender_id)

        else:
            group = self.group
            group_name = await self.client(JoinChannelRequest(group))
            users = await self.client.get_participants(self.group, aggressive=True)
            print(len(users))
            if len(users) < 20:
                messages = await self.client.get_messages(entity=self.group.split('/')[-1], limit=5000)
                for message in messages:
                    if message.sender_id:
                        await add_users(users=message.sender_id)
        await self.disconnect()

    async def main(self):
        if self.account.status != 'Banned':
            await self.connect()
            await self.connect_to_group()
            await asyncio.sleep(random.uniform(2, 4))
            await self.send_messages()


async def start(user: int, count: int, group: str):
    '''Запуск спама'''

    await delete_users()
    await delete_history()

    accounts = await get_accounts_db()
    message = get_message(social='telegram', user=user)

    await TClient(account=accounts[int(random.uniform(0, len(accounts)))], message=message, group=group,
                  count=count, users=[]).get_users()

    users = await get_users(count=count)


    await asyncio.sleep(random.uniform(2,5))
    chunks = [list(chunk) for chunk in np.array_split(users, len(accounts))]
    print(chunks)
    next_chunk = 0
    async with asyncio.TaskGroup() as task:
        for account in accounts:
            task.create_task(TClient(account=account, message=message, group=group, count=count, users=chunks[next_chunk]).main())
            next_chunk += 1
asyncio.run(start(user=944360812, count=10, group='https://t.me/kazanchat57'))


async def add_accounts():
    accounts = get_accounts()
    proxys = get_proxy()
    ready_accounts = await get_accounts_db()

    account_count = 0
    proxy_count = 0

    while account_count < len(accounts):
        try:
            async with aiofiles.open(f'input/telegram_accounts/{accounts[account_count]}.json', 'r') as file:
                data = await file.read()
                js = json.loads(data)
        except FileNotFoundError:
            account_count += 1

        finally:
            await add_account(app_hash=js['app_hash'], proxy=proxys[proxy_count], app_version=js['sdk'], phone=accounts[account_count], device_model=js['device'])

        account_count += 1
        proxy_count += 1

# asyncio.run(add_accounts())
