from fastapi import APIRouter

from app.users.queries import UsersQueries
from app.users.schemas import SUserAuth
from app.users.utils import hash_password

router = APIRouter(
	prefix='/users',
	tags=['Пользователи']
)


@router.post('/registration')
async def register_user(user_data: SUserAuth):
	if not await UsersQueries.find_one_or_none(email=user_data.email):
		hashed_password = hash_password(user_data.password)
		await UsersQueries.add(
			first_name=user_data.first_name,
			last_name=user_data.last_name,
			email=user_data.email,
			hashed_password=hashed_password,
		)
		return 'Регистрация прошла успешно'
	else:
		return 'Данный пользователь уже зарегистрирован'
