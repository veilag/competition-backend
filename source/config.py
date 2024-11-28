from dotenv import load_dotenv
from os import getenv

load_dotenv()


class Config:
    DATABASE_URL: str = getenv("DATABASE_URL")
    DOMAIN: str = getenv("DOMAIN")
    MODE: str = getenv("MODE")

    TELEGRAM_TOKEN: str = getenv("TELEGRAM_TOKEN")
    STAND_TOKEN: str = getenv("STAND_TOKEN")
