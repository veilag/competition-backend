from dotenv import load_dotenv
from os import getenv

load_dotenv()


class Config:
    DATABASE_URL: str = getenv("DATABASE_URL")
    MODE: str = getenv("MODE")
