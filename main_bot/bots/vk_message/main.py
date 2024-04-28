import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from main_bot.files import get_message
from main_bot.etc.functions import get_accounts_vk


service = Service(executable_path='')
driver = webdriver.Firefox()

def login():
    '''Авторизация в вк'''
def vk_thread(user: str, password: str):
    '''Запуск VK спама'''

    message = get_message(social='vk')
    users = parse_all_users()
    accounts = get_accounts_vk()

    for account in accounts:
        try:
            driver.maximize_window()
            driver.get("https://vk.com")
            time.sleep(2)
            email_input = driver.find_element(By.ID, 'index_email')
            email_input.clear()
            email_input.send_keys(user)
            email_input.send_keys(Keys.ENTER)
            time.sleep(3)

            password_input = driver.find_element(By.NAME, 'password')
            password_input.clear()
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
            time.sleep(3)

            for user in users:
                search_input = driver.find_element(By.CLASS_NAME, 'vkuiSearch__control')
                search_input.clear()
                search_input.send_keys(user)
                time.sleep(1)
                user_input = driver.find_elements(By.ID, 'modal_catalog_user')[0].click()
                time.sleep(1.5)
                try:
                    message_button = driver.find_elements(By.CLASS_NAME, 'ProfileHeaderButton')[1].click()
                    time.sleep(3)

                    message_input = driver.find_element(By.ID, 'mail_box_editable')
                    time.sleep(2)
                    message_input.clear()
                    message_input.send_keys(message)
                    time.sleep(2)
                    message_input.send_keys(Keys.ENTER)
                except Exception as _ex:
                    continue

        except Exception as _ex:
            print(_ex)
        finally:
            driver.close()
            driver.quit()


def parse_all_users(group: str) -> list | dict:
    '''Получение всех пользователей из группы VK'''

    page = requests.get(group)
