from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from config import settings

engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass
