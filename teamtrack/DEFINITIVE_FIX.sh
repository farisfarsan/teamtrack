#!/bin/bash

# DEFINITIVE PythonAnywhere Fix Script
# This script will fix ALL deployment issues

echo "🚀 Starting DEFINITIVE PythonAnywhere fix..."

# Set the project directory
PROJECT_DIR="/home/gryttteamtrak/gryttteamtrack/teamtrack"
cd $PROJECT_DIR

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Pull latest changes from git
echo "📥 Pulling latest changes from git..."
git pull origin master

# Set environment variables
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

# Test the application
echo "🧪 Testing application..."
python manage.py check --deploy

echo "✅ DEFINITIVE fix completed!"
echo ""
echo "📋 CRITICAL: Update your PythonAnywhere WSGI file with the content from DEFINITIVE_WSGI_FIX.py"
echo "Then reload your web app in the PythonAnywhere dashboard"
echo ""
echo "🔑 Admin login:"
echo "Username: admin"
echo "Password: admin123"
echo "URL: https://yourdomain.pythonanywhere.com/admin/"
