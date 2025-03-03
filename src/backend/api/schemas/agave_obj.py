from typing import Optional

from pydantic import BaseModel


class AgaveObjModel(BaseModel):
    name: str
    username: str
    username_source: str
    image_file_path: str
    source: str
    sourcename: str
    image_source: Optional[str]
    origin_country: Optional[str] = None
    is_display: bool
    search_count: Optional[int] = 0
