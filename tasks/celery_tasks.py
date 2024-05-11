from pydantic import EmailStr
import smtplib
from config import settings
from tasks.email_templates import create_booking_confirmation_template
from tasks.my_celery import celery
from PIL import Image
from pathlib import Path


@celery.task
def process_pic(
        path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((300, 100))
    im_resized_1000_500.save(f'static/images/resized_1000_500_{im_path.name}')
    im_resized_200_100.save(f'static/images/resized_200_100_{im_path.name}')


@celery.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr
):
    email_to_mock = settings.SMTP_USER
    email_message = create_booking_confirmation_template(booking, email_to_mock)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(email_message)

