from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
	
	email: EmailStr
	password: str


class SUserRegister(SUserAuth):

	first_name: str
	last_name: str

