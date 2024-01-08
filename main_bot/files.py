import os


def new_message_telegram(message: str) -> None:
    path_to_file = os.path.join(os.getcwd(), 'main_bot/bots/telegram_message/message.txt')

    with open(path_to_file, 'w') as f:
        f.write(message.split('Сообщение')[1])


def new_message_vk(message: str) -> None:
    path_to_file = os.path.join(os.getcwd(), 'main_bot/bots/vk_message/message.txt')

    with open(path_to_file, 'w') as f:
        f.write(message.split('Сообщение')[1])


def get_message() -> str:
    message_file= os.path.join(os.getcwd(), 'main_bot/bots/telegram_message/message.txt')

    with open(message_file, 'r') as f:
        message = f.read()

    return message