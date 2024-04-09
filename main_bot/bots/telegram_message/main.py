import datetime
import json
import random
import shutil
import asyncio
import aiofiles
import socks

from telethon import TelegramClient
from telethon.errors import PhoneNumberBannedError, ChannelBannedError, UserDeactivatedBanError, AuthKeyUnregisteredError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, CheckChatInviteRequest

from main_bot.files import get_message
from main_bot.etc.functions import get_accounts, get_proxy


class TClient:
    def __init__(self, account: str, app_hash: str, proxy: str, device_model: str, app_version: str, group: str, message: str):
        self.account = account
        self.app_id = 6
        self.app_hash = app_hash
        self.proxy = (socks.SOCKS5, proxy.split(':')[0], 50101, True, 'demidovicpav', '7afed7819af815908dc1715aa')
        self.system_version = '4.16.30-vxCUSTOM'
        self.device_model = device_model
        self.app_version = app_version

        self.group = group
        self.message = message

    async def connect(self):
        try:
            self.client = TelegramClient(f'../../../input/telegram_accounts/{self.account}.session',
                                        api_id=6,
                                        api_hash=self.app_hash,
                                        app_version=self.app_version,
                                        device_model=self.device_model,
                                        system_version=self.system_version,
                                        proxy=self.proxy,
                                        )
            await self.client.connect()
            await self.client.get_entity('me')
        except FileNotFoundError:
            return False

    async def disconnect(self):
        await self.client.disconnect()

    async def connect_to_group(self):
        try:
            entity = await self.client.get_entity(self.group)
            await asyncio.sleep(random.uniform(1, 2))
            group = await self.client(JoinChannelRequest(channel=entity))

        except Exception as e:
            entity = await self.client(CheckChatInviteRequest(hash=self.group.split('/')[-1]))
            await asyncio.sleep(random.uniform(1, 2))
            group = await self.client(ImportChatInviteRequest(hash=self.group.split('/')[-1]))

    async def send_messages(self):
        self.messages = 0
        self.me = await self.client.get_me()

        try:
            user = await self.client.get_entity('@c0ral0vii')
            await asyncio.sleep(random.uniform(3, 6))
            await self.client.send_message(user, 'hihi')
            # for user in users:
            #     await asyncio.sleep(random.uniform(3, 6))
            #     user = await self.client.get_entity(user)
            #     await asyncio.sleep(random.uniform(1, 2))
            #
            #     query = await self.client.inline_query("@PostBot", self.message[-1])
            #     result = await query[0].click(user)
            #
            #     async with aiofiles.open(f'all_participants.txt', 'a') as file:
            #         data = await file.writelines(f'{self.me.username} - {user.username}, {datetime.datetime.now()}')
            #
            #
            #     self.messages += 1
            #     await asyncio.sleep(random.uniform(180, 200))
        except PhoneNumberBannedError or UserDeactivatedBanError:
            await shutil.move(f'../../../input/telegram_accounts/{self.account}.session',
                              f'../../../input/telegram_accounts/banned/{self.account}.session')
            await shutil.move(f'../../../input/telegram_accounts/{self.account}.json',
                              f'../../../input/telegram_accounts/banned/{self.account}.json')
            return

    async def main(self):
        await self.connect()
        await self.send_messages()
        await self.disconnect()

async def start(user: int, count: int, group: str):
    '''Запуск спама'''

    message = get_message(social='telegram', user=user)
    accounts = get_accounts()
    proxys = get_proxy()

    loop = asyncio.get_event_loop()
    clients = []
    for proxy in proxys:
        for account in accounts:
            try:
                async with aiofiles.open(f'../../../input/telegram_accounts/{account}.json', 'r') as file:
                    data = await file.read()
                    js = json.loads(data)
            except FileNotFoundError:
                continue

            client = TClient(account=account,
                             app_hash=js['app_hash'],
                             device_model=js['device'],
                             app_version=js['sdk'],
                             group=group,
                             message=message,
                             proxy=proxy,
                             )

            clients.append(client)

    await asyncio.gather(*(client.main() for client in clients))

asyncio.run(start(user=1, count=0, group='test'))