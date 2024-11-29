from typing import Optional
from pydantic import BaseModel
from ..competitions.schemas import CompetitionModel


class RoleModel(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    id: int
    public_id: str
    telegram_id: int
    name: str
    surname: str
    in_place: bool
    approved: bool

    role: RoleModel
    competition: Optional[CompetitionModel] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    telegram_id: int
    name: str
    surname: str
    role_id: int
    competition_id: Optional[int] = None
