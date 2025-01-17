from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from sqladmin import Admin

from app.admin.views import BookingAdmin, CarsAdmin, LocationsAdmin, ReviewsAdmin, UsersAdmin
from app.bookings.router import router as bookings_router
from app.cars.router import router as cars_router
from app.reviews.router import router as reviews_router
from app.users.router import router as users_router
from app.images.router import router as image_router
from app.pages.user import router as page_user_router
from app.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
	redis = aioredis.from_url('redis://localhost:6379', encoding='utf-8', decode_responses=True)
	FastAPICache.init(RedisBackend(redis), prefix='cache')
	yield


api = FastAPI(lifespan=lifespan)

api.include_router(router=cars_router)
api.include_router(router=bookings_router)
api.include_router(router=reviews_router)
api.include_router(router=image_router)
api.include_router(router=users_router)

api.include_router(router=page_user_router)

api.mount("/static", StaticFiles(directory="app/static"), "static")

origins = ['http://localhost:3000']

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)

admin = Admin(api, engine)
admin.add_view(UsersAdmin)
admin.add_view(BookingAdmin)
admin.add_view(CarsAdmin)
admin.add_view(LocationsAdmin)
admin.add_view(ReviewsAdmin)
