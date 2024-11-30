from app.queries.base import BaseQueries
from app.bookings.models import Bookings


class BookingsQueries(BaseQueries):

	model = Bookings
