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

# Ensure all users exist with correct credentials
python manage.py ensure_users --settings=teamtrack.settings_render

# Test login functionality
python manage.py test_logins --settings=teamtrack.settings_render
