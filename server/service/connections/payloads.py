from typing import TypedDict


class StateChangePayload(TypedDict):
    state: str


class NewUserInPlacePayload(TypedDict):
    id: int
    name: str
    surname: str
    competition: str
