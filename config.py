from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
DB_NAME = getenv('DB_NAME')
DB_USER = getenv('DB_USER')
DB_PASS = getenv('DB_PASS')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
GROQ_API = getenv('GROQ_API')
ADMIN_IDS = [int(x) for x in getenv('ADMIN_IDS', '').split(',') if x.strip()]