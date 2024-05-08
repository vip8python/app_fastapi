from sqlalchemy import Column, Integer, String, JSON, ForeignKey
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
