import uuid
from typing import List, Optional
import sqlalchemy.dialects.postgresql as pg

from sqlalchemy import Column,String
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class BookTag(SQLModel, table=True):
    __tablename__ = "booktag"
    book_id: uuid.UUID = Field(default=None, foreign_key="book.uid", primary_key=True)
    tag_id: uuid.UUID = Field(default=None, foreign_key="tags.uid", primary_key=True)


class User(SQLModel, table=True):
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    username: str
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)

    role: str = Field(default="user",sa_column=Column(String, nullable=False, server_default="user") ) # DB-side default
    is_verified: bool = False
    email: str
    password_hash: str
    created_at :datetime = Field(default_factory=datetime.now)

    # this for linking back books to user who added any book
    books: List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    reviews: List["Review"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})



class Book(SQLModel, table=True):
    uid: Optional[uuid.UUID] = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="user.uid")

    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy": "selectin"})
    tags: List["Tag"] = Relationship(back_populates="books", link_model=BookTag, sa_relationship_kwargs={"lazy": "selectin"} )




class Review(SQLModel, table = True):
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    rating: int = Field(le=5)
    review_text: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    user_uid:Optional[uuid.UUID] = Field(default=None,foreign_key="user.uid")
    book_uid:Optional[uuid.UUID] = Field(default=None,foreign_key="book.uid")
    created_at:datetime = Field(default_factory=datetime.now)
    updated_at:datetime = Field(default_factory=datetime.now)
    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")



class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    books: List["Book"] = Relationship(back_populates="tags",link_model= BookTag,sa_relationship_kwargs={"lazy": "selectin"})





