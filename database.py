from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, AsyncSession
from dotenv import load_dotenv
import os
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import settings

load_dotenv()

engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass
