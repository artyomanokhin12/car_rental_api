from fastapi import FastAPI

from app.users.router import router as users_router

api = FastAPI()

api.include_router(router=users_router)
