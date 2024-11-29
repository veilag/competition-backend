from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .middlewares import DbSessionMiddleware
from ..config import Config
from .handlers import admin_router
from ..database.engine import async_session

dp = Dispatcher()

dp.update.middleware(DbSessionMiddleware(async_session))
dp.include_router(admin_router)

bot = Bot(token=Config.TELEGRAM_TOKEN)


@dp.message(CommandStart())
async def handle_start_message(message: Message) -> None:
    await message.answer(
        text="Привет, {message.from_user.full_name}",
        reply_markup=InlineKeyboardBuilder()
        .button(
            text="Открыть приложением",
            web_app=WebAppInfo(
                url=f"{Config.SERVER_DOMAIN}/templates/app" if Config.MODE == "DEV" else Config.MINIAPP_DOMAIN
            )
        )
        .as_markup()
    )
