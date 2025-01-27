from fastapi import HTTPException, status


class CarRentalException(HTTPException):
	status_code = 500
	detail = ''

	def __init__(self):
		super().__init__(status_code=self.status_code, detail=self.detail)


class AuthentificateError(CarRentalException):
	status_code = status.HTTP_401_UNAUTHORIZED
	detail = 'Mail does not exist or password is incorrect'


class InvalidTokenError(CarRentalException):
	status_code = status.HTTP_401_UNAUTHORIZED
	detail = 'Token invalid'


class UserIsNotPresentException(CarRentalException):
	status_code = status.HTTP_401_UNAUTHORIZED


class ReevaluationError(CarRentalException):
	status_code = status.HTTP_409_CONFLICT
	detail = 'The estimate for this order has already been placed'


class EstimateOnOrderInProcess(CarRentalException):
	status_code = status.HTTP_409_CONFLICT
	detail = "Can't put a grade on an order with this status"


class DateFromCannotBeAfterDateTo(CarRentalException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'The start date of the lease cannot be later than the end date of the lease'


class LargePeriodError(CarRentalException):
	status_code = status.HTTP_400_BAD_REQUEST
	detail = 'Too long a period to rent'


class CancelBookingError(CarRentalException):
	status_code = status.HTTP_400_BAD_REQUEST
	detail = 'You cannot cancel an order with this status'


class CarsFullyBooked(CarRentalException):
	status_code = status.HTTP_409_CONFLICT
	detail = 'There are no cars left'
