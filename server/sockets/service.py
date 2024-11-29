import asyncio
from typing import Dict, Callable, Coroutine, Any, List, TypedDict
from aiogram.utils.web_app import WebAppInitData
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException, status


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
        websocket: Any,
        connections: Dict[WebSocket, WebAppInitData],
        stand_connections: Dict[WebSocket, StandData]
    ):
        handler = self.handlers.get(event)

        if handler:
            kwargs = {
                "event": event,
                "data": data,
                "websocket": websocket,
                "connections": connections,
                "stand_connections": stand_connections
            }

            await handler(event, data, websocket, connections, stand_connections)
        else:
            raise ValueError(f"Нет обработчика для события: {event}")


class SocketBroker:
    def __init__(self):
        self.active_connections: Dict[WebSocket, WebAppInitData] = {}
        self.active_stand_connections: Dict[WebSocket, StandData] = {}
        self.routers: List[SocketRouter] = []

    async def connect(self, websocket: WebSocket, user_data: WebAppInitData):
        if not self.telegram_id_free(user_data.user.id):
            self.raise_and_disconnect()

        await websocket.accept()
        self.active_connections[websocket] = user_data

    async def connect_stand(self, websocket: WebSocket, stand_data: StandData):
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
        self.routers.append(router)

    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            await connection.send_json(message)

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
                    await websocket.send_json({"error": "Event name missing"})
                    continue

                handled = False
                for router in self.routers:
                    if event in router.handlers:
                        await router.dispatch(
                            event,
                            payload,
                            websocket,
                            self.active_connections,
                            self.active_stand_connections
                        )
                        handled = True

                if not handled:
                    await websocket.send_json({"error": f"No handler for event: {event}"})

        except WebSocketDisconnect:
            self.disconnect(websocket)
