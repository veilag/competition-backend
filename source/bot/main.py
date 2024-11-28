from os import getenv
from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = getenv("TELEGRAM_TOKEN")
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start_message(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}")

