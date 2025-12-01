from fastapi import FastAPI
from sqlalchemy import func
from sqlmodel import select

from src.books.routes import book_router
from src.books.seed import test_books

from src.db.main import engine, get_session, async_session_maker  # async engine
from src.auth.routes import auth_router
from src.db.models import Book
from src.errors import register_error_handlers
from src.middleware import register_middleware
from src.reviews.routes import review_router
from src.tags.routes import tags_router


version = 'v1'

app = FastAPI(
    title="Bookly",
    description="""
    Welcome! A REST API for a book review web service.
    
    This REST API is able to:
        - Create Read Update And delete books
        - Add reviews to books
        - Add tags to Books and much more!.
        """,
    version=version,
    debug=True,
    contact = {
        "name": "Aliyeva Nargiza",
        "url": "https://github.com/nnrlyv",
        "email": "nargizalieva310@gmail.com",
    })

register_error_handlers(app)
register_middleware(app)

app.include_router(book_router, prefix="/books", tags=["books"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])


async def seed_data():
    async with async_session_maker() as session:
        result = await session.exec(select(func.count()).select_from(Book))
        total = result.one()

        if total == 0:
            for book in test_books:
                session.add(book)  # добавляем по одному
            await session.commit()
            print("Seeded default books")
        else:
            print("Books already exist")
