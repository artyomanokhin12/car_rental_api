from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Locations(Base):
	__tablename__ = 'locations'

	id: Mapped[int] = mapped_column(primary_key=True)
	city: Mapped[str]

	def __repr__(self):
		return self.city
