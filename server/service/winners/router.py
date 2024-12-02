from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket
from aiogram.utils.web_app import WebAppInitData
from ...sockets.service import StandData
from ...sockets import SocketRouter
from .crud import get_revealed_winners_by_competition, create_winner, get_winners_by_competitions, update_winners_reveal_by_competition
from ..users.crud import get_user_by_public_id
from .schemas import WinnerModel

router = SocketRouter()


@router.on("WINNERS:GET_REVEALED")
async def revealed_winners_by_competition(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    winners = await get_revealed_winners_by_competition(session, data.get("competition_id"))
    await websocket.send_json({
        "event": "WINNERS:GET_REVEALED",
        "status": "success",
        "data": {
            "winners": [WinnerModel.from_orm(winner).dict() for winner in winners]
        }
    })


@router.on("WINNERS:SET_USER")
async def set_user_as_winner(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    user = await get_user_by_public_id(session, data.get("public_id"))
    await create_winner(
        session,
        user.competition_id,
        user.id,
        data.get("place")
    )

    await websocket.send_json({
        "event": "WINNERS:SET_USER:RESULT",
        "status": "success",
        "data": None
    })


@router.on("WINNERS:REVEAL_COMPETITION")
async def reveal_winner(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    winners = await get_winners_by_competitions(session, data.get("competition_id"))
    await update_winners_reveal_by_competition(session, data.get("competition_id"))

    winner_ids = {winner.user.telegram_id for winner in winners}
    winner_details = [{
        "telegram_id": winner.user.telegram_id,
        "name": winner.user.name,
        "surname": winner.user.surname,
        "place": winner.place
    } for winner in winners]

    for connection in connections:
        if connections[connection].user.id in winner_ids:
            await connection.send_json({
                "event": "WINNERS:TOKE_PLACE",
                "data": None
            })

        else:
            await connection.send_json({
                "event": "WINNERS:PLACE_REVEAL",
                "data": {
                    "competition_id": data.get("competition_id"),
                    "winners": winner_details
                }
            })
