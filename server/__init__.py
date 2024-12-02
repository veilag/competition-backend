from aiogram.types import Update
from aiogram.utils.web_app import WebAppInitData
from sqlalchemy.exc import IntegrityError

from .config import Config
from .service.auth.deps import authorize_user_connection, authorize_stand_connection
from .service.competitions.crud import init_states
from .service.users.crud import init_users_and_roles
from .sockets import SocketBroker, StandData
from .service import user_router, competition_router, winner_router
from .database import init_db, init_db_in_dev, engine
from .database.engine import async_session
from .bot import bot, dp
from fastapi import FastAPI, WebSocket, Depends

app = FastAPI(
    title="API для олимпиады",
    description="API для интерактивного проведения олимпиад или хакатонов",
    version=Config.VERSION,
    contact={
        "name": Config.Credentials.CONTACT_NAME,
        "url": Config.Credentials.CONTACT_SITE,
        "email": Config.Credentials.CONTACT_EMAIL
    },
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    }
)

socket_broker = SocketBroker()
socket_broker.register_router(user_router)
socket_broker.register_router(competition_router)
socket_broker.register_router(winner_router)

WEBHOOK_PATH = f"/bot/{Config.TELEGRAM_TOKEN}"
WEBHOOK_URL = f"{Config.SERVER_DOMAIN}{WEBHOOK_PATH}"


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )

    if Config.MODE == "PROD":
        await init_db()

    else:
        await init_db_in_dev()

    async with async_session() as session:
        try:
            await init_states(session)
            await init_users_and_roles(session)

        except IntegrityError:
            print("DATABASE INIT VALUES ALREADY EXISTS")


@app.post(
    path=WEBHOOK_PATH,
    include_in_schema=False
)
async def bot_webhook(update: dict):
    update = Update.model_validate(update, context={"bot": bot})
    await dp.feed_update(bot=bot, update=update)


@app.websocket("/connect_user")
async def handle_connection(
    websocket: WebSocket,
    auth_data: WebAppInitData = Depends(authorize_user_connection)
):
    await socket_broker.connect(websocket, auth_data)
    await socket_broker.handle_websocket(websocket)


@app.websocket("/connect_stand")
async def handle_stand_connection(
    websocket: WebSocket,
    auth_data: StandData = Depends(authorize_stand_connection)
):
    await socket_broker.connect_stand(websocket, auth_data)
    await socket_broker.handle_websocket(websocket)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
    await engine.dispose()
