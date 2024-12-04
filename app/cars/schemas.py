from datetime import date
from fastapi import Query
from pydantic import BaseModel, ConfigDict

from app.cars.models import Category


class CarsResponse(BaseModel):

	brand: str
	model: str
	category: Category
	description: str | None
	price_per_day: int
	location_id: int
	quantity: int
	available: int | str = Query('all cars')


class CarsRequest(BaseModel):

	model_config = ConfigDict(extra='forbid')

	brand: str | None = None
	model: str | None = None
	category: Category | None = None
	start_date: date | None = None
	end_date: date | None = None
	min_price_per_day: int | None = Query(None, description='Например, 10000')
	max_price_per_day: int | None = Query(None, description='Например, 150000')
	location_id: int | None = None
