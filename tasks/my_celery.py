from celery import Celery

from config import settings

celery = Celery(
    settings.MAIN,
    broker=settings.BROKER,
    include=[settings.INCLUDE]
)
