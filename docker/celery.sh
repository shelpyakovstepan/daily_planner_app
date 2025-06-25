#!/bin/sh

if [[ "${1}" == "celery" ]]; then
  celery -A app.tasks.celery_app:celery beat & celery -A app.tasks.celery_app:celery worker --loglevel=info --pool=solo
elif [[ "${1}" == "flower" ]]; then
  celery -A app.tasks.celery_app:celery flower
fi