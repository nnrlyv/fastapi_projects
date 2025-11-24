from fastapi import FastAPI
from src.books.routes import book_router

from src.db.main import engine  # async engine
from src.auth.routes import auth_router
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