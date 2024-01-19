import os


def get_accounts() -> list:
    '''Получение аккаунтов из input/telegram_accounts'''

    try:
        accounts = os.listdir(os.path.abspath('../../input/telegram_accounts'))

        return accounts
    except Exception as _ex:
        print(_ex)


def get_accounts_vk() -> list:
    '''Получене аккаунтов для vk'''

    try:
        with open('../../input/vk_accounts.txt', 'r') as f:
            accounts = [f.read().split('\n')]

            return accounts
    except Exception as _ex:
        print(_ex)


def get_accounts_ok() -> list:
    '''Получене аккаунтов для ok'''

    try:
        with open('../../input/ok_accounts.txt', 'r') as f:
            accounts = [f.read().split('\n')]

            return accounts
    except Exception as _ex:
        print(_ex)

