#!/usr/bin/env bash
# PythonAnywhere Deployment Script
# This script helps deploy your Django app to PythonAnywhere

echo "🐍 PythonAnywhere Deployment Script"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from your Django project root."
    exit 1
fi

echo "✅ Found Django project"

# Create PythonAnywhere settings if it doesn't exist
if [ ! -f "teamtrack/settings_pythonanywhere.py" ]; then
    echo "📝 Creating PythonAnywhere settings..."
    # Settings file already created above
fi

echo "✅ PythonAnywhere settings ready"

# Run migrations
echo "🔄 Running migrations..."
python3.10 manage.py migrate --settings=teamtrack.settings_pythonanywhere

# Collect static files
echo "📁 Collecting static files..."
python3.10 manage.py collectstatic --noinput --settings=teamtrack.settings_pythonanywhere

# Create superuser (optional)
echo "👤 Creating superuser..."
python3.10 manage.py createsuperuser --settings=teamtrack.settings_pythonanywhere

echo "✅ Deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Reload your web app"
echo "3. Your app will be live at: https://yourusername.pythonanywhere.com"
echo ""
echo "🎉 Your Django app is now deployed and always online!"
