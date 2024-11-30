from fastapi import FastAPI

from app.bookings.router import router as bookings_router
from app.users.router import router as users_router

api = FastAPI()

api.include_router(router=bookings_router)
api.include_router(router=users_router)
