#!/bin/bash

# PythonAnywhere Deployment Script for TeamTrack
# This script helps automate the deployment process

set -e  # Exit on any error

echo "🚀 Starting TeamTrack deployment to PythonAnywhere..."

# Configuration variables (update these)
PYTHONANYWHERE_USERNAME="yourusername"
PROJECT_NAME="teamtrack"
PYTHON_VERSION="3.10"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    print_error "Please run this script from the project root directory (where manage.py is located)"
    exit 1
fi

print_status "Project structure verified ✓"

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs
mkdir -p media
mkdir -p staticfiles

# Update settings for production
print_status "Updating settings for production..."

# Replace placeholder username in settings_production.py
if [ -f "teamtrack/settings_production.py" ]; then
    sed -i "s/yourusername/$PYTHONANYWHERE_USERNAME/g" teamtrack/settings_production.py
    print_status "Updated settings_production.py with your username ✓"
else
    print_warning "settings_production.py not found. Please create it first."
fi

# Replace placeholder username in wsgi_production.py
if [ -f "teamtrack/wsgi_production.py" ]; then
    sed -i "s/yourusername/$PYTHONANYWHERE_USERNAME/g" teamtrack/wsgi_production.py
    print_status "Updated wsgi_production.py with your username ✓"
else
    print_warning "wsgi_production.py not found. Please create it first."
fi

# Generate a secret key if .env doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file..."
    SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    cat > .env << EOF
SECRET_KEY=$SECRET_KEY
DEBUG=False
DATABASE_URL=mysql://$PYTHONANYWHERE_USERNAME:yourpassword@$PYTHONANYWHERE_USERNAME.mysql.pythonanywhere.com/$PYTHONANYWHERE_USERNAME\$teamtrack
EOF
    print_status "Created .env file with generated secret key ✓"
else
    print_status ".env file already exists ✓"
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found!"
    exit 1
fi

print_status "Requirements file found ✓"

# Display next steps
echo ""
echo "=========================================="
echo "📋 NEXT STEPS FOR PYTHONANYWHERE:"
echo "=========================================="
echo ""
echo "1. 📁 Upload your code to PythonAnywhere:"
echo "   - Option A: Git clone your repository"
echo "   - Option B: Upload files via PythonAnywhere Files tab"
echo ""
echo "2. 🐍 Set up virtual environment:"
echo "   cd ~/$PROJECT_NAME"
echo "   python$PYTHON_VERSION -m venv ${PROJECT_NAME}_env"
echo "   source ${PROJECT_NAME}_env/bin/activate"
echo ""
echo "3. 📦 Install dependencies:"
echo "   pip install --user -r requirements.txt"
echo ""
echo "4. 🗄️  Set up MySQL database:"
echo "   - Go to PythonAnywhere Dashboard → Databases"
echo "   - Create MySQL database named 'teamtrack'"
echo "   - Update .env file with your database credentials"
echo ""
echo "5. 🔄 Run migrations:"
echo "   python manage.py migrate --settings=teamtrack.settings_production"
echo ""
echo "6. 👤 Create superuser:"
echo "   python manage.py createsuperuser --settings=teamtrack.settings_production"
echo ""
echo "7. 📁 Collect static files:"
echo "   python manage.py collectstatic --settings=teamtrack.settings_production --noinput"
echo ""
echo "8. 🌐 Configure web app:"
echo "   - Go to PythonAnywhere Dashboard → Web tab"
echo "   - Create new web app (Manual configuration)"
echo "   - Use teamtrack/wsgi_production.py as WSGI file"
echo "   - Configure static files mapping"
echo ""
echo "9. 🔧 Update configuration files:"
echo "   - Replace 'yourusername' with your actual PythonAnywhere username"
echo "   - Update database credentials in .env file"
echo "   - Update SECRET_KEY in .env file"
echo ""
echo "10. 🚀 Reload your web app and test!"
echo ""
echo "📖 For detailed instructions, see: PYTHONANYWHERE_DEPLOYMENT.md"
echo ""
print_status "Deployment preparation complete! 🎉"
