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


class CarsRequest(BaseModel):

	model_config = ConfigDict(extra='forbid')

	brand: str | None = None
	model: str | None = None
	category: Category | None = None
	min_price_per_day: int | None = Query(None, description='Например, 10000')
	max_price_per_day: int | None = Query(None, description='Например, 150000')
	location_id: int | None = None
