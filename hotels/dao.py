from datetime import date

from certifi import where
from sqlalchemy import select, or_, and_, func, outerjoin, cte

from bookings.models import Bookings
from dao.base import BaseDAO
from database import async_session_maker
from hotels.models import Hotels, Rooms, RoomInfo


class HotelDAO(BaseDAO):
    model_cls = Hotels

    @classmethod
    async def search_for_hotels(cls, location: str, date_from: date, date_to: date):
        # select hotel_id, hotels.rooms_quantity - count(anon_2.room_id) as rooms_left, hotels.rooms_quantity
        # left outer join rooms on rooms.hotel_id = hotels.id
        # left outer join(
        # select * from bookings
        # where (date_from < '20232-02-15' and date_to > '2023-02-15')
        # or  (date_from >= '2023-02-15' and date_from < '2023-03-17' )
        # ) as anon_2
        # on anon_2.room_id = rooms.id
        # where (hotels.location like 'test')
        # group by hotel_id, hotels.rooms_quantity

        async with async_session_maker() as session:
            bookings_for_selected_dates = (
                select(Bookings)
                .filter(
                    or_(
                        and_(
                            Bookings.date_from < date_from, Bookings.date_to > date_from
                        ),
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from < date_to,
                        ),
                    )
                )
                .subquery('filtered_bookings')
            )
        hotels_rooms_left = (
            select(
                (
                        Hotels.rooms_quantity - func.count(bookings_for_selected_dates.c.room_id)

                ).label('rooms_left'),
                Rooms.hotel_id,
            ).select_from(Hotels)
            .outerjoin(Rooms, Rooms.hotel_id == Hotels.id)
            .outerjoin(
                bookings_for_selected_dates,
                bookings_for_selected_dates.c.room_id == Rooms.id,
            ).where(Hotels.location.contains(location.title()),
                    ).group_by(Hotels.rooms_quantity, Rooms.hotel_id)
            .cte('hotels_rooms_left')
        )
        get_hotels_info = (
            select(
                Hotels.__table__.columns,  # all colums table hotels
                hotels_rooms_left.c.rooms_left,  # extra column with count rooms
            ).select_from(Hotels)
            .join(hotels_rooms_left, hotels_rooms_left.c.chotel_id == Hotels.id)
            .where(hotels_rooms_left.c.rooms_left > 0)
        )
        hotels_info = await session.execute(get_hotels_info)
        return hotels_info.all()

    @classmethod
    async def search_for_rooms(cls, hotel_id: int, date_from: date, date_to: date) -> list[RoomInfo]:
        async with async_session_maker() as session:
            bookings_for_selected_dates = (
                select(Bookings)
                .filter(
                    or_(
                        and_(
                            Bookings.date_from < date_from, Bookings.date_to > date_from
                        ),
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from < date_to,
                        ),
                    )
                )
                .subquery('filtered_bookings')
            )
            rooms_left = (
                select(
                    (
                            Rooms.quantity - func.count(bookings_for_selected_dates.c.rooms_id))
                    .label('rooms_left'),
                    Rooms.id.label('room_id'),
                )
                .select_from(Rooms)
                .outerjoin(
                    bookings_for_selected_dates,
                    bookings_for_selected_dates.c.rooms_id == Rooms.id,
                )
                .where(Rooms.hotel_id == hotel_id)
                .group_by(
                    Rooms.quantity, bookings_for_selected_dates.c.room_id, Rooms.id
                )
                .cte()
            )

            get_rooms_info = (
                select(
                    rooms_left.c.rooms_left,
                    rooms_left.c.room_id
                )
            )

            rooms_info = await session.execute(get_rooms_info)
            return rooms_info.all()


