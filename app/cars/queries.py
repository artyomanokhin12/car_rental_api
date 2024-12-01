from app.cars.models import Cars
from app.queries.base import BaseQueries


class CarsQueries(BaseQueries):

	model = Cars

	@classmethod
	async def find_all_by_filters(cls, **data):
		query_data = data.copy()
		for param in data:
			if not data.get(param):
				query_data.pop(param)
		return await super().find_all_by_filters(**query_data)