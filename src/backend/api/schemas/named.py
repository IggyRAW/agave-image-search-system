from pydantic import BaseModel


class Named(BaseModel):
    name: str
