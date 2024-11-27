from fastapi import HTTPException, status


class CarRentalException(HTTPException):
	status_code = 500
	detail = ''

	def __init__(self):
		super().__init__(status_code=self.status_code, detail=self.detail)


class AuthentificateError(CarRentalException):
	status_code = status.HTTP_401_UNAUTHORIZED
	detail = 'Mail does not exist or password is incorrect'