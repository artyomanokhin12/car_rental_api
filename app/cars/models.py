from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Cars(Base):
	__tablename__ = 'cars'

	id: Mapped[int] = mapped_column(primary_key=True)
	model: Mapped[str]
	brand: Mapped[str]
	category: Mapped[str]
	description: Mapped[str | None]
	price_per_day: Mapped[int]
	image_url: Mapped[str | None]
	locatioon_id: Mapped[int]
