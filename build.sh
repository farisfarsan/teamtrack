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

# Create admin user
python manage.py create_admin --settings=settings_render
