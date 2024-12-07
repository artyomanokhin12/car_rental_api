from fastapi import FastAPI

from app.bookings.router import router as bookings_router
from app.cars.router import router as cars_router
from app.reviews.router import router as reviews_router
from app.users.router import router as users_router
from app.pages.user import router as page_user_router

api = FastAPI()

api.include_router(router=cars_router)
api.include_router(router=bookings_router)
api.include_router(router=reviews_router)
api.include_router(router=users_router)
api.include_router(router=page_user_router)
