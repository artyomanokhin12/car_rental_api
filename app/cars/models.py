import enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Category(enum.Enum):

	economy = 'economy'
	compact = 'compact'
	luxury = 'luxury'


class Cars(Base):
	__tablename__ = 'cars'

	id: Mapped[int] = mapped_column(primary_key=True)
	model: Mapped[str]
	brand: Mapped[str]
	category: Mapped[Category]
	description: Mapped[str | None]
	price_per_day: Mapped[int]
	image_url: Mapped[str | None]
	location_id: Mapped[int] = mapped_column(ForeignKey('locations.id', ondelete='SET NULL'))
