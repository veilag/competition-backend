from typing import Optional
from pydantic import BaseModel


class RoleBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MentorBase(BaseModel):
    id: int
    name: str
    surname: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    public_id: str
    telegram_id: int
    name: str
    surname: str
    mentor_id: Optional[int]
    in_place: bool
    approved: bool
    competition_id: int

    mentor: Optional[MentorBase] = None
    role: RoleBase

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    telegram_id: int
    name: str
    surname: str

    role: str
    mentor_id: Optional[int] = None
    competition_id: int
