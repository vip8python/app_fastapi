from fastapi import FastAPI, Query
from typing import Optional
from datetime import date
from booking.router import router as router_bookings
import asyncio
from gevent import monkey


app = FastAPI()

app.include_router(router_bookings)


@app.get('/hotels')
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        has_spa: Optional[bool] = None,
        stars: Optional[int] = Query(None, ge=1, le=5),
):
    return 'Hotel'





