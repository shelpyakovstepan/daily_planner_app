from celery import Celery
from kombu import Connection

from app.config import settings
from app.logger import logger

def check_rabbit_connection():
    conn_url = f"amqp://{settings.RABBIT_USER}:{settings.RABBIT_PASS}@{settings.RABBIT_HOST}:{settings.RABBIT_PORT}/"
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
        broker=f"amqp://{settings.RABBIT_USER}:{settings.RABBIT_PASS}@{settings.RABBIT_HOST}:{settings.RABBIT_PORT}/",
        include=["app.tasks.tasks"],
    )
else:
    raise RuntimeError("Cannot initialize Celery without RabbitMQ connection")
