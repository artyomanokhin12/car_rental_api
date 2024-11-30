from datetime import date
import enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Status(enum.Enum):

	pending = 'pending'
	in_process = 'in_process'
	confirmed = 'confirmed'
	canceled = 'canceled'


class Bookings(Base):
	__tablename__ = 'bookings'

	id: Mapped[int] = mapped_column(primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))
	car_id: Mapped[int] = mapped_column(ForeignKey('cars.id', ondelete='SET NULL'))
	start_date: Mapped[date]
	end_date: Mapped[date]
	total_price: Mapped[int]
	status: Mapped[Status]
