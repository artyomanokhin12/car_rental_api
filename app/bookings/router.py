from fastapi import APIRouter, Depends, Query
from pydantic import TypeAdapter, parse_obj_as

from app.bookings.models import Bookings, Status
from app.bookings.queries import BookingsQueries
from app.bookings.schemas import BookingsResponse, NewBookingCar
from app.exceptions import DateFromCannotBeAfterDateTo, LargePeriodError
from app.tasks.tasks import send_booking_confirmation_email
from app.users.models import Users
from app.users.utils import get_current_user

router = APIRouter(
	prefix='/booking',
	tags=['Бронирование авто']
)


@router.get('')
async def get_all_users_bookings(
	user: Users = Depends(get_current_user)
) -> list[BookingsResponse]:
	all_bookings = await BookingsQueries.find_all_by_filters(user_id=user.id)
	return all_bookings


@router.post('')
async def add_new_booking(
	BookingData: NewBookingCar = Query(), 
	user: Users = Depends(get_current_user)
) -> BookingsResponse:
	if BookingData.end_date < BookingData.start_date:
		raise DateFromCannotBeAfterDateTo
	elif (BookingData.end_date - BookingData.start_date).days > 30:
		raise LargePeriodError
	new_booking: Bookings = await BookingsQueries.add_new_booking(user=user, **BookingData.model_dump())
	booking_json = TypeAdapter(BookingsResponse).validate_python(new_booking).model_dump()
	send_booking_confirmation_email(booking_json, user.email)
	return booking_json


@router.post('/cancel/{booking_id}')
async def cancel_booking(booking_id: int, user: Users = Depends(get_current_user)):
	await BookingsQueries.cancel_booking(user, booking_id)
	return 'Бронирование отменено'


@router.post('/status/{boooking_id}')
async def change_booking_status(
	booking_id: int,
	status: Status,
	user: Users = Depends(get_current_user)
):
	await BookingsQueries.change_status(user, booking_id, status)
	return 'Статус успешно изменен'
