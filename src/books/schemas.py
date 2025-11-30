import uuid
from datetime import datetime
from typing import List
from pydantic import BaseModel


class TagSchema(BaseModel):
    uid: uuid.UUID
    name: str

class ReviewSchema(BaseModel):
    uid: uuid.UUID
    review_text: str
    rating: int

#for pagination part without rev and tags
class BookSchema(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str

#for rev and tags
class BookDetailSchema(BaseModel):
    uid: uuid.UUID
    title: str
    publisher: str
    reviews: list[ReviewSchema] = []
    tags: list[TagSchema] = []



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


class PaginatedBooksResponse(BaseModel):
    items: List[BookSchema]
    total: int
    page: int
    limit: int
    pages: int

