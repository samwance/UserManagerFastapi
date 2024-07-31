from pydantic import BaseModel


class UserCreate(BaseModel):
    full_name: str


class User(UserCreate):
    id: int

    class Config:
        from_attributes = True
