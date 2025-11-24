import uuid
from datetime import datetime

from pydantic import BaseModel

from src.reviews.schemas import ReviewModel
from src.tags.schemas import TagModel


class BookSchema(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str
    tags: list[TagModel]
    reviews: list[ReviewModel]



class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


class BookCreateModel(BaseModel):
    title:str
    author:str
    publisher: str
    published_date: str
    page_count: int
    language: str


