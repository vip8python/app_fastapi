from datetime import date
from exceptions import RoomCannotBeBooked
from fastapi import APIRouter, Depends
from bookings.dao import BookingDAO
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)):  #:
    return await BookingDAO.find_all(user_id=user.id)


@router.post('')
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
