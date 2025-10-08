#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --settings=teamtrack.settings_render

# Run migrations
python manage.py migrate --settings=teamtrack.settings_render

# Create superuser if it doesn't exist (optional)
python manage.py shell --settings=teamtrack.settings_render << EOF
from accounts.models import User
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser(
        email='admin@example.com',
        name='Admin User',
        password='admin123'
    )
    print('Superuser created')
else:
    print('Superuser already exists')
EOF
