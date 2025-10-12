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

# Create users for production
python manage.py setup_render_users --settings=teamtrack.settings_render

# Test authentication
python manage.py test_auth --settings=teamtrack.settings_render
