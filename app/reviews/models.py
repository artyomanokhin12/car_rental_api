from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Reviews(Base):
	__tablename__ = 'reviews'

	id: Mapped[int] = mapped_column(primary_key=True)
	booking_id: Mapped[int] = mapped_column(ForeignKey('bookings.id', ondelete='CASCADE'))
	rating: Mapped[int]
	comment: Mapped[str | None]
