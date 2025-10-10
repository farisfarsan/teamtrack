#!/usr/bin/env bash
# Production start script for Render

# Set the Django settings module
export DJANGO_SETTINGS_MODULE=settings_render

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the application
exec gunicorn wsgi:application --bind 0.0.0.0:$PORT
