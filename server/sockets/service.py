import asyncio
from typing import Dict, Callable, Coroutine, Any, List, TypedDict, Tuple
from aiogram.utils.web_app import WebAppInitData
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException, status

from ..service.users.models import User
from ..database.engine import async_session


class StandData(TypedDict):
    type: str
    id: str


class SocketRouter:
    def __init__(self):
        self.handlers: Dict[str, Callable[..., Coroutine[Any, Any, None]]] = {}

    def on(self, event: str):
        def decorator(func: Callable[..., Coroutine[Any, Any, None]]):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError("Обработчик события должен представлять собой асинхронную функцию")

            self.handlers[event] = func
            return func

        return decorator

    async def dispatch(
        self,
        event: str,
        data: Any,
        websocket: WebSocket,
        connections: Dict[WebSocket, WebAppInitData],
        stand_connections: Dict[WebSocket, StandData]
    ):
        handler = self.handlers.get(event)

        if handler:
            async with async_session() as session:
                await handler(event, data, session, websocket, connections, stand_connections)
        else:
            raise ValueError(f"Нет обработчика для события: {event}")


class SocketBroker:
    def __init__(self):
        self.active_connections: Dict[WebSocket, WebAppInitData] = {}
        self.active_stand_connections: Dict[WebSocket, StandData] = {}
        self.global_handlers: Dict[str, Callable[..., Coroutine[Any, Any, None]]] = {}

    async def connect(self, websocket: WebSocket, auth_data: WebAppInitData):
        print("Connections:", self.active_connections)
        if not self.telegram_id_free(auth_data.user.id):
            self.raise_and_disconnect()

        await websocket.accept()
        self.active_connections[websocket] = auth_data

    async def connect_stand(self, websocket: WebSocket, stand_data: StandData):
        print("Stand connections:", self.active_stand_connections)
        if not self.stand_id_free(stand_data["id"]):
            self.raise_and_disconnect()

        await websocket.accept()
        self.active_stand_connections[websocket] = stand_data

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            del self.active_connections[websocket]

        if websocket in self.active_stand_connections:
            del self.active_stand_connections[websocket]

    def register_router(self, router: SocketRouter):
        for event, handler in router.handlers.items():
            if event in self.global_handlers:
                raise ValueError(f"Найден дублирующий обработчик для события: {event}")
            self.global_handlers[event] = handler

    def stand_id_free(self, stand_id: str):
        for connection in self.active_stand_connections:
            if self.active_stand_connections[connection]["id"] == stand_id:
                return False

        return True

    def telegram_id_free(self, telegram_id: int):
        for connection in self.active_connections:
            if self.active_connections[connection].user.id == telegram_id:
                return False

        return True

    def raise_and_disconnect(self):
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    async def handle_websocket(self, websocket: WebSocket):
        try:
            while True:
                data = await websocket.receive_json()
                event = data.get("event")
                payload = data.get("data")

                if not event:
                    await websocket.send_json({"error": "Не указано событие"})
                    continue

                handler = self.global_handlers.get(event)
                if handler:
                    async with async_session() as session:
                        await handler(
                            event,
                            payload,
                            session,
                            websocket,
                            self.active_connections,
                            self.active_stand_connections
                        )
                else:
                    await websocket.send_json({"error": f"Сервер не поддерживает такое событие: {event}"})

        except WebSocketDisconnect:
            self.disconnect(websocket)
