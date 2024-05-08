from datetime import date
from sqlalchemy import Column, Integer, ForeignKey, Date, Computed
from database import Base


class Bookings(Base):
    __tablename__ = 'bookings'

    id: int = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey('rooms.id'))
    user_id = Column(ForeignKey('users.id'))
    date_from: date = Column(Date, nullable=False)
    date_to: date = Column(Date, nullable=False)
    price: int = Column(Integer, nullable=False)
    total_cost: int = Column(Integer, Computed('(date_to - date_from) * price'))
    total_days: int = Column(Integer, Computed('date_to - date_from'))
