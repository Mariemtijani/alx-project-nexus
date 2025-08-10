#!/usr/bin/env bash
set -e

# go where manage.py lives
cd /app/app

# apply migrations & collect static
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# start server
exec gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000}
