from typing import Dict
from aiogram.utils.web_app import WebAppInitData
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket
from ...sockets.service import StandData
from ...sockets import SocketRouter
from .schemas import UserModel, UserCreate, UserInPlace
from .crud import get_users_in_place, create_user, get_user_count, get_user_by_telegram_id, get_user_by_public_id

router = SocketRouter()


@router.on("USERS:GET_ME")
async def competition_change(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    user = await get_user_by_telegram_id(session, connections[websocket].user.id)

    if not user:
        await websocket.send_json({
            "event": "USERS:GET_ME:RESULT",
            "status": "error",
            "data": {
                "message": "Пользователь не зарегистрирован"
            }
        })
        return

    await websocket.send_json({
        "event": "USERS:GET_ME:RESULT",
        "status": "success",
        "data": UserModel.from_orm(user).dict()
    })


@router.on("USERS:REGISTER")
async def competition_change(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    user = await get_user_by_telegram_id(session, connections[websocket].user.id)

    if not user:
        data["telegram_id"] = connections[websocket].user.id

        try:
            await create_user(session, UserCreate(**data))
            await session.commit()

            await websocket.send_json({
                "event": "USERS:REGISTER:RESULT",
                "status": "success",
                "data": {
                    "message": "Пользователь успешно зарегистрирован"
                }
            })

            for stand_connection in stand_connections:
                if stand_connections[stand_connection]["type"] == "registration":
                    await stand_connection.send_json({
                        "event": "USERS:COUNT_UPDATE",
                        "data": {
                            "count": await get_user_count(session)
                        }
                    })
            return

        except IntegrityError as e:
            await websocket.send_json({
                "event": "USERS:REGISTER:RESULT",
                "data": {
                    "status": "error",
                    "message": f"Ошибка: {e}"
                }
            })
            return

    else:
        if user.role_id == 1:
            await create_user(session, UserCreate(**data))

            await websocket.send_json({
                "event": "USERS:REGISTER:RESULT",
                "status": "success",
                "data": {
                    "message": "Пользователь успешно зарегистрирован"
                }
            })
            return

    await websocket.send_json({
        "event": "USERS:REGISTER:RESULT",
        "status": "error",
        "data": {
            "message": "Пользователь уже зарегистрирован"
        }
    })


@router.on("USERS:GET_IN_PLACE")
async def fetch_user_count(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    users = await get_users_in_place(session)
    await websocket.send_json({
        "event": "USERS:GET_IN_PLACE:RESULT",
        "data": {
            "users": [UserModel.from_orm(user).dict() for user in users]
        }
    })


@router.on("USERS:GET_COUNT")
async def fetch_user_count(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    await websocket.send_json({
        "event": "USERS:GET_COUNT:RESULT",
        "data": {
            "count": await get_user_count(session)
        }
    })


@router.on("USERS:SET_IN_PLACE")
async def user_in_place(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    user = await get_user_by_telegram_id(session, connections[websocket].user.id)
    if user.role.type == "admin" or user.role.type == "staff":
        user_to_update = await get_user_by_public_id(session, data.get("public_id"))
        user_to_update.in_place = True
        await session.commit()

        for connection in connections:
            if connections[connection].user.id == user_to_update.telegram_id:
                await connection.send_json({
                    "event": "USERS:IN_PLACE_UPDATE",
                    "status": "success",
                    "data": None
                })

                await websocket.send_json({
                    "event": "USERS:SET_IN_PLACE:RESULT",
                    "status": "success",
                    "data": {
                        "message": "Пользователь отмечен на вход",
                        "user": UserInPlace.from_orm(user_to_update).dict()
                    }
                })

                for stand_connection in stand_connections:
                    if stand_connections[stand_connection]["type"] == "registration":
                        await stand_connection.send_json({
                            "event": "USERS:NEW_IN_PLACE",
                            "status": "success",
                            "data": UserInPlace.from_orm(user_to_update).dict()
                        })
    else:
        await websocket.send_json({
            "event": "USERS:SET_IN_PLACE:RESULT",
            "status": "error",
            "data": {
                "message": "У вас нет прав на выполнение этого действия",
            }
        })
