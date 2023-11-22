from pydantic import BaseModel


class Message(BaseModel):
    message: str


class User(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Result(BaseModel):
    created: bool
