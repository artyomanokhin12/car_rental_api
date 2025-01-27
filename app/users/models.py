from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Users(Base):
	__tablename__ = 'users'

	id: Mapped[int] = mapped_column(primary_key=True)
	email: Mapped[str] = mapped_column(unique=True)
	hashed_password: Mapped[bytes]
	first_name: Mapped[str]
	last_name: Mapped[str]

	def __repr__(self) -> str:
		return f'{self.first_name} {self.last_name}'
