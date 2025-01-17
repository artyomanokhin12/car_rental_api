from sqladmin import ModelView

from app.bookings.models import Bookings
from app.cars.models import Cars
from app.locations.models import Locations
from app.reviews.models import Reviews
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
	column_list = [Users.id, Users.first_name, Users.last_name, Users.email]
	column_details_exclude_list = [Users.hashed_password]
	can_delete = False
	can_create = False
	name = 'Пользователи'
	name_plural = 'Пользователи'
	icon = 'fa-solid fa-users'


class BookingAdmin(ModelView, model=Bookings):
	column_list = [Bookings.id, Bookings.users, Bookings.cars, Bookings.status]
	can_delete = False
	name = 'Бронирование'
	name_plural = 'Бронирования'
	icon = 'fa-solid fa-note-sticky'


class CarsAdmin(ModelView, model=Cars):
	column_list = [c.name for c in Cars.__table__.c]
	name = 'Авто'
	name_plural = 'Автомобили'
	icon = 'fa-solid fa-car'


class LocationsAdmin(ModelView, model=Locations):
	column_list = [Locations.id, Locations.city]
	name = 'Локация'
	name_plural = 'Локация'
	icon = 'fa-solid fa-city'


class ReviewsAdmin(ModelView, model=Reviews):
	column_list = [c.name for c in Reviews.__table__.c]
	can_create = False
	name = 'Рецензии'
	name_plural = 'Рецензии'
