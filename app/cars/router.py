from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.cars.queries import CarsQueries
from app.cars.schemas import CarsRequest, CarsResponse, DetailCarResponse

router = APIRouter(
	prefix='/cars',
	tags=['Машины']
)


@router.get('')
@cache(expire=30)
async def get_all_cars(
	data: CarsRequest = Query()
) -> list[CarsResponse]:
	cars = await CarsQueries.find_all_by_filters(**(data.model_dump()))
	return cars


@router.get('/{id}')
@cache(expire=360)
async def get_car_info_by_id(id: int) -> DetailCarResponse:
	car = await CarsQueries.find_by_id(id)
	return car
