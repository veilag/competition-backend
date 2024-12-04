from pydantic import BaseModel


class CompetitionModel(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    public_id: str
    name: str
    surname: str
    competition: CompetitionModel

    class Config:
        from_attributes = True


class WinnerModel(BaseModel):
    user: UserModel
    revealed: bool
    place: int

    class Config:
        from_attributes = True


class NominationWinnerModel(BaseModel):
    name: str
    revealed: bool
    user: UserModel

    class Config:
        from_attributes = True
