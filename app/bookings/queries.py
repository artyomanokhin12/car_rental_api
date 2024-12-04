from datetime import date, timedelta
from sqlalchemy import and_, func, insert, or_, select, update
from app.cars.models import Cars
from app.database import async_session_maker
from app.exceptions import CancelBookingError
from app.queries.base import BaseQueries
from app.bookings.models import Bookings, Status
from app.users.models import Users


class BookingsQueries(BaseQueries):

	model = Bookings

	@classmethod
	async def add_new_booking(
		cls,
		user: Users,
		car_id: int,
		start_date: date,
		end_date: date,
	):
		async with async_session_maker() as session:
			active_bookings = (
				select(Bookings)
				.where(
					and_(
						Bookings.car_id == car_id,
						Bookings.status.in_((Status.in_process, Status.pending)),
						or_(
							and_(
								Bookings.start_date >= start_date,
								Bookings.start_date <= end_date,
							),
							and_(
								Bookings.start_date < start_date,
								Bookings.end_date >= start_date,
							)
						)
					)
				)
				.cte('active_bookings')
			)
			get_free_cars = (
				select((Cars.quantity - func.count(active_bookings.c.car_id)).label('free_cars'))
				.join(active_bookings, active_bookings.c.car_id==Cars.id, isouter=True)
				.where(Cars.id==car_id)
				.group_by(Cars.quantity, active_bookings.c.car_id)
			)
			result = await session.execute(get_free_cars)
			free_cars: int = result.scalar()

			if free_cars > 0:
				total_price = select(Cars.price_per_day).filter_by(id=car_id)
				result = await session.execute(total_price)
				price: int = result.scalar()
				total_price = price * (end_date - start_date).days
				add_new_car_booking = (
					insert(Bookings).values(
						user_id=user.id,
						car_id=car_id,
						start_date=start_date,
						end_date=end_date,
						total_price=total_price,
						status=Status.pending.value,
					)
					.returning(Bookings)
				)
				new_booking = await session.execute(add_new_car_booking)
				await session.commit()
				return new_booking.scalar()
			else:
				return 'На данный момент свободных машин нет'
			
	@classmethod
	async def cancel_booking(cls, user: Users, booking_id: int):
		async with async_session_maker() as session:
			get_current_status = select(Bookings.status).filter_by(id=booking_id)
			result = await session.execute(get_current_status)
			get_current_status = result.scalar()
			if get_current_status == Status.pending.value:
				stmt = (
					update(Bookings)
					.filter_by(id=booking_id, user_id=user.id)
					.values(status=Status.canceled.value)
				)
				await session.execute(stmt)
				await session.commit()
			else:
				raise CancelBookingError
	

	@classmethod
	async def change_status(cls, user: Users, booking_id: int, new_status: Status):
		async with async_session_maker() as session:
			current_booking_status = select(Bookings.status).filter_by(id=booking_id, user_id=user.id)
			result = await session.execute(current_booking_status)
			current_booking_status = result.scalar()
			print(current_booking_status)
			print(new_status)
			if (
				(
					current_booking_status == Status.in_process
					and 
					new_status == Status.confirmed
				)
				or
				(
					current_booking_status == Status.pending
					and
					new_status == Status.in_process
				)
			):
				stmt = (
					update(Bookings)
					.where(Bookings.id==booking_id)
					.values(status=new_status)
				)
				await session.execute(stmt)
				await session.commit()
			else:
				raise CancelBookingError
