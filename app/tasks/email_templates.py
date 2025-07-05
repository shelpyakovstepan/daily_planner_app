# STDLIB
from email.message import EmailMessage

# THIRDPARTY
from pydantic import EmailStr

# FIRSTPARTY
from app.config import settings


def create_registration_email(email_to: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Уведомление о регистрации"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        """
            <h1> Регистрация прошла успешно </h1>
             Вы зарегистрировались в приложении-ежедневнике
        """,
        subtype="html",
    )

    return email
