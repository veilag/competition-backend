from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..config import Config

dp = Dispatcher()
bot = Bot(token=Config.TELEGRAM_TOKEN)


@dp.message(CommandStart())
async def handle_start_message(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}")
