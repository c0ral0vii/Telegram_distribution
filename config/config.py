import os
import glob

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DEFAULT_PATH = os.getcwd()

print(DEFAULT_PATH)
SQLACHEMY_URL = f'sqlite+aiosqlite:///{DEFAULT_PATH}/db.sqlite3'