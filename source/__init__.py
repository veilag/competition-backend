from fastapi import FastAPI
from .sockets import SocketBroker
from .routers import home_router

app = FastAPI(
    title="API для приложения олимпиады",
    version="1.0.0",
    contact={
        "name": "Галиев Рамиль",
        "url": "https://t.me/veilag"
    }
)

broker = SocketBroker()
# app ...

app.include_router(home_router)
