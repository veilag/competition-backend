from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from ..config import Config

dp = Dispatcher()

bot = Bot(
    token=Config.TELEGRAM_TOKEN,
    default=DefaultBotProperties(
        parse_mode="Markdown"
    )
)


@dp.message(CommandStart())
async def handle_start_message(message: Message) -> None:
    await message.answer(
        text="👋 *Добро пожаловать на IT Олимпиады*\n\nВсе взаимодействие идет через наше мини-приложение!\n\n✅ Вы можете открыть его нажав на кнопку ниже или в описании бота",
        reply_markup=InlineKeyboardBuilder()
        .button(
            text="🚀 Открыть приложение",
            web_app=WebAppInfo(
                url=f"{Config.SERVER_DOMAIN}/templates/app" if Config.MODE == "DEV" else Config.MINIAPP_DOMAIN
            )
        )
        .as_markup()
    )
