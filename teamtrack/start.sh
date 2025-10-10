#!/usr/bin/env bash
# Production start script for Render

# Set the Django settings module
export DJANGO_SETTINGS_MODULE=teamtrack.settings_render

# Start the application directly with gunicorn
exec gunicorn teamtrack.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
