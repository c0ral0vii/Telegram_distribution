import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

SQLACHEMY_URL = 'sqlite+aiosqlite:///db.sqlite3'