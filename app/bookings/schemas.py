from datetime import date
from pydantic import BaseModel

from app.cars.models import Category


class NewBookingCar(BaseModel):

	car_id: int
	start_date: date
	end_date: date
