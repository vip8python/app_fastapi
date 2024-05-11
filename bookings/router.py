from datetime import date

from pydantic import parse_obj_as

from bookings.schemas import SBooking
from exceptions import RoomCannotBeBooked
from fastapi import APIRouter, Depends
from bookings.dao import BookingDAO
from tasks.celery_tasks import send_booking_confirmation_email
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
    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict

@router.delete('')
async def remove_booking(
        booking_id: int

):
    pass
