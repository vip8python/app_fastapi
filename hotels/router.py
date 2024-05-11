from datetime import date, datetime

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import aioredis
from fastapi import APIRouter, Query
import asyncio
from pydantic import parse_obj_as
from hotels.dao import HotelDAO
from hotels.models import HotelInfo, Hotel, RoomInfo

router = APIRouter(
    prefix='/hotels',
    tags=['hotels'],
)


# async def create_redis_client():
#     return await aioredis.create_redis_pool('redis://localhost')
#
#
# async def initialize_cache():
#     redis = await create_redis_client()
#     FastAPICache.init(RedisBackend(redis), prefix='cache')
#
# asyncio.run(initialize_cache())
# def get_current_date():
#     return datetime.now().date()

@router.get('/{location}')
@cache(expire=30)
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date = Query(..., description=f'Like this, {datetime.now().date()}'),
        date_to: date = Query(..., description=f'Like this, {datetime.now().date()}'),
):
    # hotels = await HotelInfo.query.gino.all()
    hotels = await HotelInfo.search_for_hotels(location, date_from, date_to)
    hotels_list = parse_obj_as(list[HotelInfo], hotels)
    return hotels_list


@router.get('/{hotel_id}/rooms')
async def get_rooms_by_time(
        hotel_id: int,
        date_from: date = Query(..., description=f'Like this, {datetime.now().date()}'),
        date_to: date = Query(..., description=f'Like this, {datetime.now().date()}'),
) -> list[RoomInfo]:
    rooms = await HotelDAO.search_for_rooms(hotel_id, date_from, date_to)
    return rooms
