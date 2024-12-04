from sqlalchemy import and_, or_, select, func
from app.bookings.models import Bookings, Status
from app.cars.models import Cars
from app.queries.base import BaseQueries
from app.database import async_session_maker


class CarsQueries(BaseQueries):

	model = Cars

	@classmethod
	async def find_all_by_filters(cls, **data):
		query_data = data.copy()
		for param in data:
			if not data.get(param):
				query_data.pop(param)
		if (
			query_data.get('start_date')
			and 
			query_data.get('end_date')
			and
			query_data.get('location_id')
		):
			booked_cars = (
				select(Bookings.car_id, func.count(Bookings.car_id).label('cars_booked'))
				.where(
					and_(
						Bookings.status.not_in((Status.confirmed, Status.canceled)),
						or_(
							and_(
								Bookings.start_date >= query_data['start_date'],
								Bookings.start_date <= query_data['end_date'],
							),
							and_(
								Bookings.start_date < query_data['start_date'],
								Bookings.end_date >= query_data['start_date'],
							)
						)
					)
				)
				.group_by(Bookings.car_id)
				.cte('booked_cars')
			)
			get_available_cars = (
				select(
					Cars.__table__.columns,
					(Cars.quantity - func.coalesce(booked_cars.c.cars_booked, 0)).label('available')
				)
				.join(booked_cars, booked_cars.c.car_id == Cars.id, isouter=True)
				.where(
					Cars.quantity - func.coalesce(booked_cars.c.cars_booked, 0) > 0,
					Cars.location_id == query_data['location_id']
				)
			)
			async with async_session_maker() as session:
				result = await session.execute(get_available_cars)
				return result.mappings().all()
		else:
			query_data.pop('start_date', None)
			query_data.pop('end_date', None)
			return await super().find_all_by_filters(**query_data)