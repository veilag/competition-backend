from dotenv import load_dotenv
from os import getenv

load_dotenv()


class Config:
    DOMAIN: str = getenv("DOMAIN")
    MODE: str = getenv("MODE")
    VERSION: str = getenv("VERSION")
    DATABASE_URL: str = getenv("DATABASE_URL")

    TELEGRAM_TOKEN: str = getenv("TELEGRAM_TOKEN")
    STAND_TOKEN: str = getenv("STAND_TOKEN")

    class Credentials:
        CONTACT_NAME: str = getenv("CONTACT_NAME")
        CONTACT_SITE: str = getenv("CONTACT_SITE")
        CONTACT_EMAIL: str = getenv("CONTACT_EMAIL")
