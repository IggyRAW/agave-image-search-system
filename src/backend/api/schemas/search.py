from typing import Optional

from pydantic import BaseModel


class CardItemModel(BaseModel):
    id: str
    name: str
    username: str
    username_source: str
    image_file_path: str
    source: str
    sourcename: str
    image_source: Optional[str]
    origin_country: Optional[str]
    search_count: int
