from fastapi import APIRouter
from sqlalchemy import select

from booking.models import Bookings
from database import async_session_maker


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)

@router.get('')
async def get_bookings():
    async with async_session_maker() as session:
        query = select(Bookings)
        result = await session.execute(query)
        return result.mappings().all()



