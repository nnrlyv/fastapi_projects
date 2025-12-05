from typing import List

from celery import Celery
from src.config import config
from src.mail import mail, create_message
from asgiref.sync import async_to_sync


c_app = Celery( "bookly_tasks",
    broker=config.REDIS_URL,
    backend=config.REDIS_URL
)

c_app.conf.update(
    broker_connection_retry_on_startup=True,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Almaty',
    enable_utc=True,
)

c_app.config_from_object("src.config")

@c_app.task()
def send_email(recipients: List[str], subject: str, body: str):

    message = create_message(recipients=recipients, subject=subject, body=body)

    async_to_sync(mail.send_message)(message)
    print("Email sent")