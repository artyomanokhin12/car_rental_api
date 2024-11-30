from fastapi import APIRouter, Depends

from app.bookings.queries import BookingsQueries
from app.users.models import Users
from app.users.utils import get_current_user

router = APIRouter(
	prefix='/booking',
	tags=['Бронирование авто']
)


@router.get('')
async def get_all_users_bookings(user: Users = Depends(get_current_user)):
	all_bookings = await BookingsQueries.find_all_by_filters(user_id=user.id)
	return all_bookings


@router.post('')
async def add_new_booking():
	...


@router.delete('/{booking_id}')
async def delete_booking():
	...
