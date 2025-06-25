# THIRDPARTY
from celery import Celery
from celery.schedules import crontab
from kombu import Connection

# FIRSTPARTY
from app.config import settings
from app.logger import logger


def check_rabbit_connection():
    conn_url = (
        f"amqp://{settings.RABBIT_USER}:{settings.RABBIT_PASS}@"
        f"{settings.RABBIT_HOST}:{settings.RABBIT_PORT}/"
        )
    try:
        with Connection(conn_url) as conn:
            conn.connect()
            logger.info("Successfully connected to RabbitMQ")
            return True
    except Exception as e:
        logger.error(f"RabbitMQ connection failed: {str(e)}", exc_info=True)
        return False


if check_rabbit_connection():
    celery = Celery(
        "tasks",
        broker=f"amqp://{settings.RABBIT_USER}:{settings.RABBIT_PASS}@"
        f"{settings.RABBIT_HOST}:{settings.RABBIT_PORT}/",
        include=["app.tasks.tasks"],
    )
else:
    raise RuntimeError("Cannot initialize Celery without RabbitMQ connection")


celery.conf.update(
    timezone="Europe/Moscow", enable_utc=True, worker_hijack_root_logger=False
)


celery.conf.beat_schedule = {
    "gl_update_statuses": {
        "task": "app.tasks.tasks.global_update_statuses_task",
        "schedule": crontab(hour=0, minute=0),
    }
}
