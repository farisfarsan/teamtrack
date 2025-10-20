#!/bin/bash

# PythonAnywhere Deployment Script for TeamTrack
# This script fixes common deployment issues

echo "🚀 Starting TeamTrack deployment fixes..."

# Set the project directory
PROJECT_DIR="/home/gryttteamtrak/gryttteamtrack/teamtrack"
cd $PROJECT_DIR

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Set environment variables for PythonAnywhere
echo "🔧 Setting up environment..."
export DJANGO_SETTINGS_MODULE=teamtrack.settings_pythonanywhere

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Setting up admin user..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin user created')
else:
    print('Admin user already exists')
EOF

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Set up attendance tables specifically
echo "📊 Setting up attendance tables..."
python manage.py setup_attendance

# Test the application
echo "🧪 Testing application..."
python manage.py check --deploy

echo "✅ Deployment fixes completed!"
echo ""
echo "📋 Next steps:"
echo "1. Update your PythonAnywhere WSGI file to use: teamtrack.settings_pythonanywhere"
echo "2. Reload your web app"
echo "3. Test the application at your domain"
echo ""
echo "🔑 Admin login:"
echo "Username: admin"
echo "Password: admin123"
echo "URL: https://yourdomain.pythonanywhere.com/admin/"
