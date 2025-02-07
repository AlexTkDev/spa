#!/bin/bash

echo "Waiting for PostgreSQL..."
until nc -z -v -w30 "$DATABASE_HOST" "$DATABASE_PORT"
do
  echo "Waiting for database connection..."
  sleep 1
done

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:9000 myproject.wsgi:application --workers 3 --timeout 30
