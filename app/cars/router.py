from datetime import date, datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Query

from app.cars.models import Cars, Category
from app.cars.queries import CarsQueries
from app.cars.schemas import CarsRequest, CarsResponse

router = APIRouter(
	prefix='/cars',
	tags=['Машины']
)


@router.get('')
async def get_all_cars(
	data: CarsRequest = Query()
) -> list[CarsResponse]:
	cars = await CarsQueries.find_all_by_filters(**(data.model_dump()))
	return cars
