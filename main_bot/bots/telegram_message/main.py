from opentele.td import TDesktop
from opentele.api import API, CreateNewSession
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch


async def get_users(group_username: str, _send_message: bool = False) -> None:
    '''Получение пользователей и запись в файл со вссеми пользователями'''

    tdataFolder = r"C:\\Users\\<username>\\AppData\\Roaming\\Telegram Desktop\\tdata"
    tdesk = TDesktop(tdataFolder)

    # Используйте официальный API iOS с случайно сгенерированной информацией об устройстве
    api = API.TelegramIOS(api_id=24598056, api_hash='b33e418a411261a505fec3a526e56019').Generate()

    # Преобразуйте сессию TDesktop в клиент telethon
    client = await tdesk.ToTelethon("newSession.session", CreateNewSession, api)

    # Подключитесь и распечатайте все вошедшие в систему устройства
    await client.connect()
    await client.PrintSessions()

    # Получите всех участников из группы
    all_participants = []
    offset = 0
    limit = 10

    while True:
        participants = await client(GetParticipantsRequest(group_username, ChannelParticipantsSearch(''), offset, limit, hash=0))

        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)

    with open('all_participants.txt', 'a') as f:
        f.write('\n'.join(all_participants))

    if _send_message:
        await send_message(client=client)
    return all_participants


async def send_message(client: API.TelegramIOS):
    '''Отправьте сообщение каждому участнику'''

    with open('message.txt', 'r') as f:
        message = f.read()

    with open('all_participants.txt', 'r') as f:
        for user in f.read():
            try:
                await client.send_message(user.id, message)
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю {user.id}: {str(e)}")

