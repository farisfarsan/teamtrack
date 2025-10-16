#!/usr/bin/env bash
# Enhanced production start script for Render with robust error handling

set -e  # Exit on any error

echo "🚀 Starting TeamTrack with enhanced error handling..."

# Set the Django settings module
export DJANGO_SETTINGS_MODULE=settings_render

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to handle errors gracefully
handle_error() {
    log "❌ Error occurred: $1"
    log "🔄 Attempting recovery..."
    
    # Try to recover database connection
    if command_exists python; then
        python manage.py migrate --settings=settings_render || true
    fi
    
    # Try to collect static files
    if command_exists python; then
        python manage.py collectstatic --noinput --settings=settings_render || true
    fi
    
    log "⚠️ Recovery attempted, continuing..."
}

# Enhanced error handling
trap 'handle_error "Script failed"' ERR

log "📋 Checking system requirements..."

# Check Python version
if command_exists python; then
    PYTHON_VERSION=$(python --version 2>&1)
    log "✅ Python found: $PYTHON_VERSION"
else
    log "❌ Python not found"
    exit 1
fi

# Check if manage.py exists
if [ ! -f "manage.py" ]; then
    log "❌ manage.py not found"
    exit 1
fi

log "✅ manage.py found"

log "🗄️ Running database migrations..."
python manage.py migrate --settings=settings_render || {
    log "⚠️ Migration failed, attempting to continue..."
}

log "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=settings_render || {
    log "⚠️ Static file collection failed, attempting to continue..."
}

log "👥 Setting up users..."
python manage.py setup_render_users --settings=settings_render || {
    log "⚠️ User setup failed, attempting to continue..."
}

log "🔍 Testing authentication..."
python manage.py test_auth --settings=settings_render || {
    log "⚠️ Authentication test failed, attempting to continue..."
}

log "🏥 Running health check..."
python manage.py shell --settings=settings_render -c "
from teamtrack.health import HealthChecker
health = HealthChecker.get_overall_health()
print(f'Health status: {health[\"overall_status\"]}')
" || {
    log "⚠️ Health check failed, attempting to continue..."
}

log "🔄 Starting enhanced keep-alive system..."
python manage.py shell --settings=settings_render -c "
from teamtrack.keep_alive_enhanced import start_enhanced_keep_alive
start_enhanced_keep_alive()
print('Enhanced keep-alive system started')
" || {
    log "⚠️ Keep-alive system failed to start, attempting to continue..."
}

log "🚀 Starting application with Gunicorn..."

# Start the application with enhanced configuration
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
    --log-level info \
    --capture-output \
    --enable-stdio-inheritance
