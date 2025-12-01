from datetime import datetime

from sqlmodel import select

from src.db.main import async_session_maker
from src.db.models import Book
import asyncio

test_books = [
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "publisher": "Prentice Hall",
        "published_date": datetime(2008, 8, 1),
        "page_count": 464,
        "language": "English",
    },
    {
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen",
        "publisher": "MIT Press",
        "published_date": datetime(2009, 7, 31),
        "page_count": 1312,
        "language": "English",
    },
    {
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "publisher": "Addison-Wesley",
        "published_date": datetime(1999, 10, 20),
        "page_count": 352,
        "language": "English",
    },
    {
        "title": "Design Patterns",
        "author": "Erich Gamma",
        "publisher": "Addison-Wesley",
        "published_date": datetime(1994, 10, 31),
        "page_count": 395,
        "language": "English",
    },
    {
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "publisher": "No Starch Press",
        "published_date": datetime(2015, 11, 1),
        "page_count": 560,
        "language": "English",
    },
    {
        "title": "You Don’t Know JS",
        "author": "Kyle Simpson",
        "publisher": "O’Reilly Media",
        "published_date": datetime(2015, 12, 28),
        "page_count": 278,
        "language": "English",
    },
    {
        "title": "Database System Concepts",
        "author": "Abraham Silberschatz",
        "publisher": "McGraw-Hill",
        "published_date": datetime(2010, 2, 16),
        "page_count": 1376,
        "language": "English",
    },
    {
        "title": "Computer Networks",
        "author": "Andrew S. Tanenbaum",
        "publisher": "Pearson",
        "published_date": datetime(2010, 3, 10),
        "page_count": 960,
        "language": "English",
    },
    {
        "title": "Artificial Intelligence: A Modern Approach",
        "author": "Stuart Russell",
        "publisher": "Pearson",
        "published_date": datetime(2015, 12, 11),
        "page_count": 1152,
        "language": "English",
    },
    {
        "title": "Operating System Concepts",
        "author": "Abraham Silberschatz",
        "publisher": "Wiley",
        "published_date": datetime(2018, 1, 1),
        "page_count": 976,
        "language": "English",
    },
]



async def seed_books():
    async with async_session_maker() as session:
        result = await session.exec(select(Book))
        exists = result.first()

        if exists:
            print("📚 Books already exist. Seed skipped.")
            return

        for data in test_books:
            session.add(Book(**data))

        await session.commit()
        print("✅ Seed completed! Added default books.")


if __name__ == "__main__":
    asyncio.run(seed_books())