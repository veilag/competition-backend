from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import Message
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
        text="👋 *Добро пожаловать на IT Олимпиады*\n\nВсе взаимодействие идет через наше мини-приложение!\n\n✅ Вы можете открыть его перейдя в профиль бота, там будет большая кнопка «Открыть приложение»",
    )


@dp.message()
async def handle_reply_message(message: Message) -> None:
    if message.reply_to_message:
        replied_user_id = message.reply_to_message.from_user.id
        await message.answer(
            text=f"⚙️ *Вы пытаетесь зарегистрирован пользователя без его ведома*\n\nTelegram ID: {replied_user_id}"
        )

    else:
        await message.answer(
            text="👋 *Добро пожаловать на IT Олимпиады*\n\nВсе взаимодействие идет через наше мини-приложение!\n\n✅ Вы можете открыть его перейдя в профиль бота, там будет большая кнопка «Открыть приложение»",
        )
