FROM python:3.12

RUN mkdir /daily_planner

WORKDIR /daily_planner

RUN pip install poetry

COPY pyproject.toml poetry.lock* README.md ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN apt-get update && apt-get install -y dos2unix && \
    dos2unix /daily_planner/docker/celery.sh && \
    chmod a+x /daily_planner/docker/*.sh

CMD ["poetry", "run", "gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]