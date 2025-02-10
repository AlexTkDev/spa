#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:9000 config.wsgi:application --workers 2 --timeout 30
