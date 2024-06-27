import os
import glob

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DEFAULT_PATH = os.getcwd()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

SQLACHEMY_URL = f'sqlite+aiosqlite:///{DEFAULT_PATH}/db.sqlite3'