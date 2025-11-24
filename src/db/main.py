
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import async_sessionmaker


DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/books_db"

engine = create_async_engine(DATABASE_URL)

# создаём фабрику для async-сессий
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# функция для получения сессии
async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

# функция для создания таблиц
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async def on_startup():
        await create_db_and_tables()