# 🚀 PythonAnywhere Deployment Guide

## ✅ **Fixed Issues**
- ✅ `ModuleNotFoundError: No module named 'teamtrack.settings_pythonanywhere'`
- ✅ `ModuleNotFoundError: No module named 'attendance.urls'`
- ✅ `RuntimeError: Model class attendance.models.AttendanceRecord doesn't declare an explicit app_label`
- ✅ Database migration issues

## 📋 **Step-by-Step Deployment**

### **Step 1: Pull Latest Changes**
```bash
cd ~/gryttteamtrack/teamtrack
git pull origin master
```

### **Step 2: Update WSGI File**
In your PythonAnywhere dashboard, go to **Web** tab and update your WSGI file:

```python
import os
import sys

# Add your project directory to the Python path
path = '/home/gryttteamtrak/gryttteamtrack/teamtrack'
if path not in sys.path:
    sys.path.insert(0, path)

# Also add the parent directory to ensure teamtrack module is found
parent_path = '/home/gryttteamtrak/gryttteamtrack'
if parent_path not in sys.path:
    sys.path.insert(0, parent_path)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamtrack.settings_pythonanywhere')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### **Step 3: Run Deployment Commands**
In your PythonAnywhere console:

```bash
# Navigate to your project
cd ~/gryttteamtrack/teamtrack

# Activate virtual environment
source venv/bin/activate

# Set Python path
export PYTHONPATH="/home/gryttteamtrak/gryttteamtrack:$PYTHONPATH"

# Run migrations
python manage.py makemigrations --settings=teamtrack.settings_pythonanywhere
python manage.py migrate --settings=teamtrack.settings_pythonanywhere

# Create superuser (optional)
python manage.py createsuperuser --settings=teamtrack.settings_pythonanywhere

# Collect static files
python manage.py collectstatic --settings=teamtrack.settings_pythonanywhere --noinput

# Test the setup
python manage.py check --settings=teamtrack.settings_pythonanywhere
```

### **Step 4: Reload Web App**
In your PythonAnywhere dashboard, click the **Reload** button for your web app.

## 🔧 **Environment Variables**
Make sure you have these environment variables set in your PythonAnywhere console:

```bash
export DJANGO_ENV="production"
export DB_NAME="gryttteamtrak$teamtrack"
export DB_USER="gryttteamtrak"
export DB_PASSWORD="your_mysql_password"
export DB_HOST="gryttteamtrak.mysql.pythonanywhere.com"
export DB_PORT="3306"
```

## 🧪 **Testing**
After deployment, test these URLs:
- `https://gryttteamtrak.pythonanywhere.com/` - Should redirect to dashboard
- `https://gryttteamtrak.pythonanywhere.com/admin/` - Admin interface
- `https://gryttteamtrak.pythonanywhere.com/health/` - Health check

## 🚨 **Troubleshooting**

### **If you get "ModuleNotFoundError":**
1. Check that your WSGI file has the correct Python path
2. Make sure you're in the right directory (`~/gryttteamtrack/teamtrack`)
3. Verify the PYTHONPATH is set correctly

### **If you get database errors:**
1. Check your MySQL database credentials
2. Run migrations: `python manage.py migrate --settings=teamtrack.settings_pythonanywhere`
3. Verify database tables exist

### **If you get template errors:**
1. Run: `python manage.py collectstatic --settings=teamtrack.settings_pythonanywhere --noinput`
2. Check that templates are in the correct directory

## 📞 **Quick Commands Reference**

```bash
# Check Django setup
python manage.py check --settings=teamtrack.settings_pythonanywhere

# Run migrations
python manage.py migrate --settings=teamtrack.settings_pythonanywhere

# Create superuser
python manage.py createsuperuser --settings=teamtrack.settings_pythonanywhere

# Collect static files
python manage.py collectstatic --settings=teamtrack.settings_pythonanywhere --noinput

# Test import
python -c 'import teamtrack.settings_pythonanywhere; print("Settings imported successfully")'
```

## 🎉 **Success Indicators**
- ✅ Django check passes without errors
- ✅ Migrations run successfully
- ✅ Static files collected
- ✅ Web app loads without errors
- ✅ Admin interface accessible

Your Django app should now be fully deployed and working on PythonAnywhere! 🚀
