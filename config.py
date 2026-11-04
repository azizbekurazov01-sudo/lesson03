import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Bot tokenini olish
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
