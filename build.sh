#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔧 Starting build process..."

# Navigate to the teamtrack directory where the Django project is located
cd teamtrack

# Upgrade pip first
pip install --upgrade pip

# Install dependencies with better error handling
echo "📦 Installing dependencies..."
pip install -r requirements.txt --no-cache-dir

# Check if DATABASE_URL is set (should be automatically set by Render)
echo "🗄️ Checking database configuration..."
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️ WARNING: DATABASE_URL not set! This may cause data loss."
    echo "DATABASE_URL should be automatically set by Render when database is linked."
else
    echo "✅ DATABASE_URL is set - PostgreSQL database will be used"
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=teamtrack.settings_render

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate --settings=teamtrack.settings_render

# Create users for production
echo "👥 Setting up users..."
python manage.py setup_render_users --settings=teamtrack.settings_render

# Test authentication
echo "🔐 Testing authentication..."
python manage.py test_auth --settings=teamtrack.settings_render

echo "✅ Build completed successfully!"
