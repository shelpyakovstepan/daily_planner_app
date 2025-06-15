#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery -A app.tasks.celery_app:celery worker --loglevel=INFO --pool=solo
  celery -A app.tasks.celery_app:celery beat --loglevel=INFO
elif [[ "${1}" == "flower" ]]; then
  celery -A app.tasks.celery_app:celery flower
fi