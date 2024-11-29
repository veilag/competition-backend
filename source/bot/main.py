from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from ..config import Config

dp = Dispatcher()
bot = Bot(token=Config.TELEGRAM_TOKEN)


@dp.message(CommandStart())
async def handle_start_message(message: Message) -> None:
    await message.answer(
        text="Привет, {message.from_user.full_name}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="Открыть приложение",
                    web_app=WebAppInfo(
                        url=f"{Config.DOMAIN}/app"
                    )
                )
            ]]
        )
    )
