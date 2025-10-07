#!/usr/bin/env python
"""
Deployment script for TeamTrack
"""
import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamtrack.settings')
    django.setup()

def collect_static():
    """Collect static files"""
    print("Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])

def migrate_database():
    """Run database migrations"""
    print("Running database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])

def create_superuser():
    """Create superuser if needed"""
    print("Creating superuser...")
    try:
        from accounts.models import User
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser(
                email='admin@example.com',
                password='admin123',
                name='Admin User'
            )
            print("Superuser created: admin@example.com / admin123")
        else:
            print("Superuser already exists")
    except Exception as e:
        print(f"Error creating superuser: {e}")

def main():
    """Main deployment function"""
    print("Starting TeamTrack deployment...")
    
    # Setup Django
    setup_django()
    
    # Run migrations
    migrate_database()
    
    # Create superuser
    create_superuser()
    
    # Collect static files
    collect_static()
    
    print("Deployment completed successfully!")
    print("\nTo start the server:")
    print("python manage.py runserver 0.0.0.0:8000")
    print("\nOr with gunicorn:")
    print("gunicorn teamtrack.wsgi:application --bind 0.0.0.0:8000")

if __name__ == '__main__':
    main()
