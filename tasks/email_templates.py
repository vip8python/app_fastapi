from email.message import EmailMessage
from pydantic import EmailStr
from config import settings


def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr,
):
    email = EmailMessage()
    email['subject'] = "confirm booking"
    email['from'] = settings.SMTP_USER
    email['to'] = email_to

    email.set_content(
        f'''
        <h1> confirm booking</h1>
        Confirm rooms from {booking['date_from']} to {booking['date_to']}
''',
        subtype='html'
    )
    return email
