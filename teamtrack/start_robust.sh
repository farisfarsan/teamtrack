#!/usr/bin/env bash
# Robust production start script for Render
# This script focuses on getting the service running reliably

set -e  # Exit on any error

echo "🚀 Starting TeamTrack..."

# Set the Django settings module
export DJANGO_SETTINGS_MODULE=settings_render

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "📋 Starting TeamTrack deployment..."

# Run migrations
log "🗄️ Running database migrations..."
python manage.py migrate --settings=settings_render || {
    log "⚠️ Migration failed, attempting to continue..."
}

# Collect static files
log "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=settings_render || {
    log "⚠️ Static file collection failed, attempting to continue..."
}

# Create users if needed
log "👥 Setting up users..."
python manage.py setup_render_users --settings=settings_render || {
    log "⚠️ User setup failed, attempting to continue..."
}

log "✅ Basic setup completed"

# Start recovery system
log "🔄 Starting task recovery system..."
python manage.py shell --settings=settings_render -c "
from teamtrack.startup_recovery import start_recovery_on_startup
start_recovery_on_startup()
print('Task recovery system started')
" || {
    log "⚠️ Recovery system failed to start, attempting to continue..."
}

log "🚀 Starting application with Gunicorn..."

exec gunicorn teamtrack.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info
