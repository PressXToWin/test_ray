#!/bin/sh

python manage.py migrate
python manage.py collectstatic --no-input --clear
cp -rf /app/collected_static/. /static/static/

celery -A test_ray worker -B & exec "$@"