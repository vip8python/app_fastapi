from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs
from dotenv import load_dotenv
import os

from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)


class Base(AsyncAttrs, DeclarativeBase):
    pass
