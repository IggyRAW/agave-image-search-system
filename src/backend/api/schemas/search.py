from pydantic import BaseModel


class CardItemModel(BaseModel):
    id: str
    name: str
    username: str
    username_source: str
    image_file_path: str
    source: str
    sourcename: str
    image_source: str
    origin_country: str
