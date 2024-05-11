from datetime import date
from sqlalchemy import insert, select, func, and_, or_
from bookings.models import Bookings
from dao.base import BaseDAO
from database import async_session_maker, engine
from hotels.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        async with async_session_maker() as session:
            """
            select rooms.quantity - count(room_id) as rooms_left from bookings
            join rooms on rooms.id = bookings.room_id
            where room_id = 4 and
            (data_from < '2024-06-01' and date_from > '2024-06-01') or
            (date_from > '2024-06-01' and date_to < '2024-06-25')
            group by room_id, rooms.quantity;
            """
        get_rooms_left = select(
            Rooms.quantity - func.count(Bookings.room_id).label('rooms_left')
        ).select_from(Bookings).join(
            Rooms, Rooms.id == Bookings.room_id, full=True
        ).where(
            and_(
                Rooms.id == room_id,
                or_(
                    Bookings.room_id.is_(None),
                    and_(
                        Bookings.date_from < date_from,
                        Bookings.date_from > date_from
                    ),
                    and_(
                        Bookings.date_from > date_from,
                        Bookings.date_from < date_to
                    )
                )
            )
        ).group_by(Rooms.id, Rooms.quantity)
        rooms_left = await session.execute(get_rooms_left)
        rooms_left = rooms_left.scalar()

        print(get_rooms_left.compile(engine, compile_kwargs={'literal_binds': True}))

        if not rooms_left or rooms_left > 0:
            get_price = await session.execute(select(Rooms.price).filter_by(id=room_id))
            add_booking = insert(Bookings).values(
                room_id=room_id,
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                price=get_price.scalar()
            ).returning(Bookings)
            new_booking = await session.execute(add_booking)
            await session.commit()
            return new_booking.scalar()


@classmethod
async def delete_booking(cls, booking_id, current_user):
    async with async_session_maker() as session:
        pass
