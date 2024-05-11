from celery import Celery

from config import settings

celery = Celery(
    settings.REDIS_MAIN,
    broker=settings.REDIS_BROKER,
    include=[settings.REDIS_INCLUDE]
)
