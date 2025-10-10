#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip first
pip install --upgrade pip

# Install dependencies with better error handling
pip install -r requirements.txt --no-cache-dir

# Collect static files
python manage.py collectstatic --noinput --settings=teamtrack.settings_render

# Run migrations
python manage.py migrate --settings=teamtrack.settings_render

# Create real users for production
python manage.py create_real_users --settings=teamtrack.settings_render
