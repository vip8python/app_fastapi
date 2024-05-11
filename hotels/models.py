from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base


class Hotels(Base):
    __tablename__: str = 'hotels'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    location: str = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity: int = Column(Integer, nullable=False)
    image_id: int = Column(Integer)


class Rooms(Base):
    __tablename__: str = 'rooms'

    id: int = Column(Integer, primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey('hotels.id'), nullable=False)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)
    price: int = Column(Integer, nullable=False)
    services = Column(JSON, nullable=True)
    quantity: int = Column(Integer, nullable=False)
    image_id: int = Column(Integer)


class HotelInfo(Base):
    __tablename__: str = 'hotel_info'

    id = Column(Integer, primary_key=True)

    @classmethod
    async def search_for_hotels(cls, session: AsyncSession, location: str, date_from, date_to):
        query = select(Hotels).join(Rooms).filter(Hotels.location == location).filter(
            Rooms.date_from <= date_from).filter(Rooms.date_to >= date_to)

        result = await session.execute(query)
        hotels = result.scalars().all()

        return hotels


class Hotel:
    pass


class RoomInfo(BaseModel):
    rooms_left: int
    room_id: int
