from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket
from aiogram.utils.web_app import WebAppInitData
from ...sockets.service import StandData
from ...sockets import SocketRouter
from .crud import (
    get_revealed_winners_by_competition, create_winner,
    update_nomination_winner_reveal_by_competition, update_winner_reveal_by_competition,
    get_winner_by_place, get_nomination_winner,
    get_winners_by_competitions, get_nomination_winners_by_competitions
)
from ..users.crud import get_user_by_id
from .schemas import WinnerModel, NominationWinnerModel

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
    user = await get_user_by_id(session, data.get("user_id"))
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


@router.on("WINNERS:SET_NOMINATION_USER")
async def set_user_as_winner(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    user = await get_user_by_id(session, data.get("user_id"))

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


@router.on("WINNERS:REVEAL_COMPETITION_WINNER")
async def reveal_competition_winner(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    winner = await get_winner_by_place(session, data.get("competition_id"), data.get("place"))

    for connection in connections:
        if connections[connection].user.id == winner.user.telegram_id:
            await connection.send_json({
                "event": "WINNERS:TOKE_PLACE",
                "data": None
            })

        else:
            await connection.send_json({
                "event": "WINNERS:PLACE_REVEAL",
                "data": {
                    "competition_id": data.get("competition_id"),
                    "place": data.get("place"),
                    "winner": {
                        "name": winner.user.name,
                        "surname": winner.user.surname,
                    }
                }
            })

    await update_winner_reveal_by_competition(session, data.get("competition_id"), data.get("place"))


@router.on("WINNERS:REVEAL_COMPETITION_NOMINATION_WINNER")
async def reveal_competition_nomination_winner(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    nomination_winner = await get_nomination_winner(session, data.get("competition_id"), data.get("name"))

    for connection in connections:
        if connections[connection].user.id == nomination_winner.user.telegram_id:
            await connection.send_json({
                "event": "WINNERS:NOMINATION_TOKE_PLACE",
                "data": None
            })

        else:
            await connection.send_json({
                "event": "WINNERS:NOMINATION_REVEAL",
                "data": {
                    "competition_id": data.get("competition_id"),
                    "winner": {
                        "name": nomination_winner.user.name,
                        "surname": nomination_winner.user.surname,
                    }
                }
            })

    await update_nomination_winner_reveal_by_competition(session, data.get("competition_id"), data.get("name"))


@router.on("WINNERS:GET_PLACES")
async def get_winners(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    winners = await get_winners_by_competitions(session, data.get("competition_id"))

    await websocket.send_json({
        "event": "WINNERS:GET_PLACES:RESULT",
        "data": {
            "winners": [WinnerModel.from_orm(winner).dict() for winner in winners]
        }
    })


@router.on("WINNERS:GET_NOMINATIONS")
async def get_nominations(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    winners = await get_nomination_winners_by_competitions(session, data.get("competition_id"))

    await websocket.send_json({
        "event": "WINNERS:GET_NOMINATIONS:RESULT",
        "data": {
            "winners": [NominationWinnerModel.from_orm(winner).dict() for winner in winners]
        }
    })
