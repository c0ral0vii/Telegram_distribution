import os


def new_message(text: str) -> None:
    path_to_file = os.path.join(os.getcwd(), 'bots/telegram_message/message.txt')

    with open(path_to_file, 'w') as f:
        f.write(text)


def get_user_id() -> set:
    path_to_file = os.path.join(os.getcwd(), 'bots/telegram_message/all_participants.txt')

    with open(path_to_file, 'r') as f:
        user_id = set(f.read().split())

    return user_id
