import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver

class InstagramAccount:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        options = Options()
        self.browser = webdriver.Firefox(options=options)

    def login(self):
        browser = self.browser
        browser.get('https://ok.ru/')
        time.sleep(random.randint(2,6))

        username_input = browser.find_element(By.NAME, 'st.email')
        username_input.clear()
        username_input.send_keys(self.username)

        time.sleep(5)
        password_input = browser.find_element(By.NAME, 'st.password')
        password_input.clear()
        password_input.send_keys(self.password)

        auth_button = browser.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(random.randint(50,100))
    def close_browser(self):

        self.browser.close()
        self.browser.quit()
InstagramAccount = InstagramAccount('+375292387952', 'Celovek3213').login()