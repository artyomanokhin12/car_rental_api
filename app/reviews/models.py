from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.bookings.models import Bookings
from app.database import Base
from app.users.models import Users


class Reviews(Base):
	__tablename__ = 'reviews'

	id: Mapped[int] = mapped_column(primary_key=True)
	booking_id: Mapped[int] = mapped_column(ForeignKey('bookings.id', ondelete='CASCADE'))
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))
	rating: Mapped[int]
	comment: Mapped[str | None]

	booking: Mapped['Bookings'] = relationship()
	user: Mapped['Users'] = relationship()

	def __repr__(self):
		return self.id
