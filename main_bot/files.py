import os

def new_message(message: str, social: str) -> None:
    path_to_file = os.path.join(os.getcwd(), f'main_bot/bots/{social}_message/message.txt')

    with open(path_to_file, 'w') as f:
        f.write(message.split(':')[1])


def get_message(social: str) -> str:
    message_file= os.path.join(os.getcwd(), f'main_bot/bots/{social}_message/message.txt')

    with open(message_file, 'r') as f:
        message = f.read()

    return message