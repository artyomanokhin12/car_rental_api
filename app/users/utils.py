from datetime import UTC, datetime, timedelta
from re import X
import bcrypt
from fastapi import Depends, Request, Response
from httpx import request
import jwt
from pydantic import EmailStr

from app.exceptions import AuthentificateError, InvalidTokenError, UserIsNotPresentException
from app.users.models import Users
from app.users.queries import UsersQueries
from app.users.schemas import SUserAuth
from app.settings import settings

TOKEN_TYPE_FIELD = 'type'
ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'
ACCESS_TOKEN_NAME = 'car_rental_access_token'
REFRESH_TOKEN_NAME = 'car_rental_refresh_token'


def hash_password(
	password: str
) -> bytes:
	salt = bcrypt.gensalt()
	pass_bytes = password.encode()
	return bcrypt.hashpw(pass_bytes, salt)


def validate_password(
	user_password: str,
	hashed_password: bytes,
) -> bool:
	return bcrypt.checkpw(user_password.encode(), hashed_password)


async def validate_auth_user(user_data: SUserAuth) -> Users:
	user: Users = await UsersQueries.find_one_or_none(email=user_data.email)
	if not user:
		raise AuthentificateError
	if not validate_password(user_data.password, user.hashed_password):
		raise AuthentificateError
	return user


def encode_jwt(
	payload: dict,
	private_key: str = settings.AUTH_JWT.private_key.read_text(),
	algorithm: str = settings.AUTH_JWT.algorithm,
	expire_minutes: int = settings.AUTH_JWT.access_token_expire_minutes,
	expire_timedelta: int | None = None,
) -> str:
	
	to_encode = payload.copy()
	now = datetime.now(UTC)
	if expire_timedelta:
		expire = now + expire_timedelta
	else:
		expire = now + timedelta(minutes=expire_minutes)
	to_encode.update(
		exp=expire,
		iat=now,
	)
	return jwt.encode(to_encode, private_key, algorithm)


def decode_jwt(
	token: str,
	public_key: str = settings.AUTH_JWT.public_key.read_text(),
	algorithm: str = settings.AUTH_JWT.algorithm,
) -> dict:
	return jwt.decode(token, public_key, algorithms=[algorithm])


def create_token(
	payload: dict,
	token_type: str,
	expire_minutes: int = settings.AUTH_JWT.access_token_expire_minutes,
	expire_timedelta: int | None = None
) -> str:
	jwt_payload = {TOKEN_TYPE_FIELD: token_type}
	jwt_payload.update(payload)
	return encode_jwt(
		jwt_payload,
		expire_minutes=expire_minutes,
		expire_timedelta=expire_timedelta,
	)


def create_access_token(user: Users) -> str:
	payload = {
		'sub': str(user.id),
		'first_name': user.first_name,
		'last_name': user.last_name,
		'email': user.email
	}
	return create_token(
		payload,
		ACCESS_TOKEN_TYPE,
		expire_minutes=settings.AUTH_JWT.access_token_expire_minutes,
	)


def create_refresh_token(user: Users) -> str:
	payload = {
		'sub': str(user.id),
		'email': user.email
	}
	return create_token(
		payload,
		REFRESH_TOKEN_TYPE,
		expire_timedelta=timedelta(days=settings.AUTH_JWT.refresh_token_expire_days)
	)


def get_token_payload(token: str, token_name: str) -> dict:
	try:
		payload: dict = decode_jwt(token)
	except jwt.InvalidTokenError:
		if token_name == ACCESS_TOKEN_NAME:
			return None
		raise InvalidTokenError
	return payload


def validate_token(request: Request):
	access_token = request.cookies.get(ACCESS_TOKEN_NAME)
	payload = get_token_payload(access_token, ACCESS_TOKEN_NAME)
	if not payload:
		refresh_token = request.cookies.get(REFRESH_TOKEN_NAME)
		payload = get_token_payload(refresh_token, REFRESH_TOKEN_NAME)
	return payload


async def create_new_access_and_refresh_token(response: Response, user: Users):
	access_token = create_access_token(user)
	refresh_token = create_refresh_token(user)
	response.set_cookie(ACCESS_TOKEN_NAME, access_token, httponly=True)
	response.set_cookie(REFRESH_TOKEN_NAME, refresh_token, httponly=True)


async def get_current_user(response: Response, payload: dict = Depends(validate_token)) -> Users:
	user_id = payload.get('sub')
	email: EmailStr = payload.get('email')
	if not (user := await UsersQueries.find_one_or_none(id=int(user_id), email=email)):
		raise UserIsNotPresentException
	token_type: str = payload.get(TOKEN_TYPE_FIELD)
	if token_type != ACCESS_TOKEN_TYPE:
		await create_new_access_and_refresh_token(response, user=user)
	return user
