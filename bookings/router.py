from fastapi import APIRouter, Depends
from bookings.dao import BookingDAO
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingDAO.find_all(user_id=user.id)
