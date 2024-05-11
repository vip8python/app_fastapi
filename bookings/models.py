from datetime import date
from sqlalchemy import Column, Integer, ForeignKey, Date, Computed
from sqlalchemy.orm import relationship

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

    # user = relationship('Users', back_populates='booking')
    # room = relationship('Rooms', back_populates='booking')
    #
    # def __str__(self):
    #     return f'Booking #{self.id}'
