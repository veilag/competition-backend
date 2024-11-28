from aiogram.types import Update

from .config import Config
from .sockets import SocketBroker
from .routers import home_router
from .database import init_db, init_db_in_dev, engine
from .bot import bot, dp
from fastapi import FastAPI

app = FastAPI(
    title="API для олимпиады",
    version="1.0.0",
    contact={
        "name": "Галиев Рамиль",
        "url": "https://t.me/veilag"
    }
)

WEBHOOK_PATH = f"/bot/{Config.TELEGRAM_TOKEN}"
WEBHOOK_URL = f"{Config.DOMAIN}{WEBHOOK_PATH}"


@app.on_event("startup")
async def on_startup():
    if Config.MODE == "PROD":
        await init_db()
        return

    await init_db_in_dev()

    webhook_info = await bot.get_webhook_info()

    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    update = Update.model_validate(update, context={"bot": bot})
    await dp.feed_update(bot=bot, update=update)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
    await engine.dispose()


app.include_router(home_router)
