import smtplib

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_app import celery
from app.tasks.email_templates import create_registration_confirmation_email


@celery.task
def send_registration_confirmation_email(
        email_to: EmailStr
):
    email = create_registration_confirmation_email(email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(email)