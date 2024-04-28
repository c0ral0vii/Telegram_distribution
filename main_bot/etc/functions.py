import os


def get_accounts() -> list:
    '''Получение аккаунтов из input/telegram_accounts'''

    try:
        accounts_path = os.listdir(os.path.abspath('input/telegram_accounts'))
        accounts = []
        # Сделать нормальную сортировку аккаунтов
        for account in accounts_path:
            if account == 'banned':
                continue
            account = account.split('.')[0]
            if account not in accounts:
                accounts.append(account)

        return accounts
    except Exception as _ex:
        print(_ex)


def get_proxy():
    '''Получение прокси для пользователей'''

    with open('input/list_proxyseller.txt', 'r') as f:
        proxy = f.read().splitlines()
    return proxy


def get_accounts_vk() -> list:
    '''Получене аккаунтов для vk'''

    try:
        with open('input/vk_accounts.txt', 'r') as f:
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

