from dotenv import load_dotenv
from os import getenv

load_dotenv()


class Config:
    SERVER_DOMAIN: str = getenv("SERVER_DOMAIN")
    MINIAPP_DOMAIN: str = getenv("MINIAPP_DOMAIN")

    MODE: str = getenv("MODE")
    VERSION: str = getenv("VERSION")
    DATABASE_URL: str = getenv("DATABASE_URL")

    TELEGRAM_TOKEN: str = getenv("TELEGRAM_TOKEN")
    TELEGRAM_ADMIN_ID: int = int(getenv("TELEGRAM_ADMIN_ID"))
    STAND_TOKEN: str = getenv("STAND_TOKEN")

    class Credentials:
        CONTACT_NAME: str = getenv("CONTACT_NAME")
        CONTACT_SITE: str = getenv("CONTACT_SITE")
        CONTACT_EMAIL: str = getenv("CONTACT_EMAIL")
