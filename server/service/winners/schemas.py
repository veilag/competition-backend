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
    place: int

    class Config:
        from_attributes = True
