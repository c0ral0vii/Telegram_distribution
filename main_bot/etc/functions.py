import os


def get_accounts():
    '''Получение аккаунтов из input/telegram_accounts'''

    try:
        accounts = os.listdir(os.path.abspath('../../input/telegram_accounts'))

        return accounts
    except Exception as _ex:
        print(_ex)



print(get_accounts())