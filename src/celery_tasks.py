from typing import List
from celery import Celery
from celery.schedules import crontab
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import config
from src.mail import mail, create_message
from asgiref.sync import async_to_sync


c_app = Celery( "bookly_tasks",
    broker=config.REDIS_URL,
    backend=config.REDIS_URL
)

c_app.conf.beat_schedule = {
    "clear-db-every-6-minutes": {
        "task": "src.celery_tasks.clear_db",
        "schedule": crontab(minute="*/6"),
    }
}

c_app.conf.update(
    broker_connection_retry_on_startup=True,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Almaty',
    enable_utc=True,
)

engine = create_async_engine(
    config.DATABASE_URL,  # пример: postgresql+asyncpg://postgres:pass@localhost/db
    echo=False,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)

c_app.config_from_object("src.config")

@c_app.task()
def clear_db():
    """Sync wrapper around async DB cleanup."""
    async_to_sync(_async_clear_db_logic)()


async def _async_clear_db_logic():
    async with async_session() as session:
        await session.execute(text('DELETE FROM "book"'))
        await session.commit()
    print("Database cleared!")


@c_app.task()
def send_email(recipients: List[str], subject: str, body: str):
    message = create_message(recipients=recipients, subject=subject, body=body)
    async_to_sync(mail.send_message)(message)
    print("Email sent")