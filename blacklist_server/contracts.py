from pydantic import BaseModel


class CheckRequest(BaseModel):
    name: str


class CheckResponse(BaseModel):
    in_list: bool
