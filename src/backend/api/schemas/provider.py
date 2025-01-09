from pydantic import BaseModel


class Provider(BaseModel):
    username: str
