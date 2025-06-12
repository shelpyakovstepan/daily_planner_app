import asyncio
import smtplib

from pydantic import EmailStr

from app.config import settings
from app.entries.dao import EntriesDAO
from app.tasks.celery_app import celery
from app.tasks.email_templates import create_registration_email


@celery.task
def send_registration_email(
        email_to: EmailStr
):
    email = create_registration_email(email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(email)

@celery.task
def global_update_statuses_task():
    async def wrapper():
        await EntriesDAO.global_update_statuses()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(wrapper())