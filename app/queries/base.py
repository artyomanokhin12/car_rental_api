from sqlalchemy import insert, select
from app.database import async_session_maker


class BaseQueries:

	model = None

	@classmethod
	async def find_one_or_none(cls, **data):
		async with async_session_maker() as session:
			query = select(cls.model).filter_by(**data)
			result = await session.execute(query)
			return result.scalar_one_or_none()

	@classmethod
	async def add(cls, **data):
		async with async_session_maker() as session:
			stmt = insert(cls.model).values(**data)
			await session.execute(stmt)
			await session.commit()

	@classmethod
	async def find_all_by_filters(cls, **data):
		async with async_session_maker() as session:
			query = select(cls.model).filter_by(**data)
			result = await session.execute(query)
			return result.scalars().all()
