from email.message import EmailMessage

from pydantic import EmailStr

from app.settings import settings

def create_booking_confirmation_template(
	booking: dict,
	email_to: EmailStr,
) -> EmailMessage:
	email = EmailMessage()
	
	email['Subject'] = 'Подтверждение брони'
	email['From'] = settings.SMTP_USER
	email['To'] = email_to

	email.set_content(
		f"""
		<h1>Подтверждение бронирования</h1>
		Вы забронировали автомобиль с {booking['start_date']} по {booking['end_date']}.
		""",
		subtype='html'
	)

	return email
