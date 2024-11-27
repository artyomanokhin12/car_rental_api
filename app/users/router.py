from fastapi import APIRouter, Depends, Response

from app.exceptions import AuthentificateError
from app.users.models import Users
from app.users.queries import UsersQueries
from app.users.schemas import SUserAuth, SUserRegister
from app.users.utils import create_access_token, create_refresh_token, hash_password, validate_auth_user

router = APIRouter(
	prefix='/users',
	tags=['Пользователи']
)


@router.post('/registration')
async def register_user(user_data: SUserRegister):
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
	

@router.post('/login')
async def user_login(response: Response, user: Users = Depends(validate_auth_user)):
	access_token = create_access_token(user)
	refresh_token = create_refresh_token(user)
	response.set_cookie('car_rental_access_token', access_token, httponly=True)
	response.set_cookie('car_rental_refresh_token', refresh_token, httponly=True)
	return user
