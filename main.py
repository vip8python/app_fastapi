from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from bookings.router import router as router_bookings
from users.router import router as router_users
from hotels.router import router as router_hotels
from pages.router import router as router_pages
from images.router import router as router_images

import aioredis

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), 'static')
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)

origins = [
    'HTTP://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=['Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers', 'Access-Control-Allow-Origin',
                   'Authorization'],
)


async def get_redis():
    return await aioredis.create_redis_pool("redis://localhost")


async def close_redis(redis):
    redis.close()
    await redis.wait_closed()


@app.on_event('startup')
async def startup_event():
    app.state.redis = await get_redis()


@app.on_event('shutdown')
async def shutdown_event():
    await close_redis(app.state.redis)


async def get_redis_pool():
    return app.state.redis


@app.get('/')
async def read_item(redis: aioredis.Redis = Depends(get_redis_pool)):
    value = await redis.get('example_key')
    return {'message': f'Value from redis: {value.decode() if value else None}'}
