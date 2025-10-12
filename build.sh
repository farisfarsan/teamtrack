#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip first
pip install --upgrade pip

# Install dependencies with better error handling
pip install -r requirements.txt --no-cache-dir

# Collect static files
python manage.py collectstatic --noinput --settings=settings_render

# Run migrations
python manage.py migrate --settings=settings_render

# Create admin user (commented out - use Django admin or manual creation)
# python manage.py createsuperuser --noinput --settings=settings_render
