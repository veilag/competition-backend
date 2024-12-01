from typing import Optional

from pydantic import BaseModel


class StateModel(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        from_attributes = True


class CompetitionModel(BaseModel):
    id: int
    name: str
    description: str
    task: Optional[str] = None
    state: StateModel

    class Config:
        from_attributes = True


class CompetitionCreate(BaseModel):
    name: str
    description: str
    task: Optional[str] = None
    state_id: int
