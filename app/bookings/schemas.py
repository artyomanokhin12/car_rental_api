from datetime import date
from pydantic import BaseModel, ConfigDict

from app.bookings.models import Status
from app.cars.models import Category


class NewBookingCar(BaseModel):

	car_id: int
	start_date: date
	end_date: date


class BookingsResponse(BaseModel):

	model_config = ConfigDict(extra='forbid', from_attributes=True)

	id: int
	car_id: int
	start_date: date
	end_date: date
	total_price: int
	status: Status
