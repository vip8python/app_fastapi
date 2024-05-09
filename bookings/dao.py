from bookings.models import Bookings
from dao.base import BaseDAO


class BookingDAO(BaseDAO):
    model = Bookings
