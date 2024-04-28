import os


def create_user(user: int) -> None:
    try:
        os.makedirs(os.path.join(os.getcwd(), f'main_bot/bots/telegram_message/temp/{user}'))
        os.makedirs(os.path.join(os.getcwd(), f'main_bot/bots/vk_message/temp/{user}'))
        os.makedirs(os.path.join(os.getcwd(), f'main_bot/bots/ok_message/temp/{user}'))

        return
    except Exception as _ex:
        print(_ex)


def new_message(message: str, social: str, user: int) -> None:
    path_to_file = os.path.join(os.getcwd(), f'main_bot/bots/{social}_message/temp/{user}/message.txt')

    with open(path_to_file, 'w', encoding='utf-8') as f:
        f.write(message.split(':')[-1])


def get_message(social: str, user: int) -> str:
    message_file= os.path.join(os.getcwd(), f'main_bot/bots/telegram_message/temp/{user}/message.txt')

    with open(message_file, 'r', encoding='utf-8') as f:
        message = f.read()

    return message.split(' ')