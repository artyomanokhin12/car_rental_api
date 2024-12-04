from fastapi import APIRouter, Depends, Query

from app.bookings.models import Bookings, Status
from app.bookings.queries import BookingsQueries
from app.exceptions import EstimateOnOrderInProcess, ReevaluationError
from app.reviews.queries import ReviewsQueries
from app.reviews.schemas import ReviewResponse
from app.users.models import Users
from app.users.utils import get_current_user

router = APIRouter(
	prefix='/reviews',
	tags=['Оценки']
)


@router.get('')
async def get_all_reviews(
	user: Users = Depends(get_current_user)
) -> list[ReviewResponse]:
	result = await ReviewsQueries.find_all_by_filters(user_id=user.id)
	return result


@router.post('')
async def add_new_review(
	booking_id: int,
	rating: int = Query(..., ge=1, le=5),
	comment: str | None = None,
	user: Users = Depends(get_current_user),
):
	booking: Bookings = await BookingsQueries.find_one_or_none(id=booking_id)
	if booking.status != Status.confirmed:
		raise EstimateOnOrderInProcess
	if await ReviewsQueries.find_one_or_none(booking_id=booking.id):
		raise ReevaluationError
	await ReviewsQueries.add(
		rating=int(rating), 
		comment=comment,
		booking_id=booking.id,
		user_id=user.id
	)
	return 'Оценка добавлена'
	