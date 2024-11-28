from .config import Config
from .sockets import SocketBroker
from .routers import home_router
from .database import init_db, init_db_in_dev
from fastapi import FastAPI

app = FastAPI(
    title="API для олимпиады",
    version="1.0.0",
    contact={
        "name": "Галиев Рамиль",
        "url": "https://t.me/veilag"
    }
)


@app.on_event("startup")
async def on_startup():
    if Config.MODE == "PROD":
        await init_db()
        return

    await init_db_in_dev()

app.include_router(home_router)
