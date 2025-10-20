# 🚨 EMERGENCY PythonAnywhere Fix Guide

## The Problem
Your WSGI file is now looking for `teamtrack.settings_pythonanywhere` but can't find it because the Python path isn't set up correctly.

## 🚨 IMMEDIATE FIX REQUIRED

### Step 1: Update Your PythonAnywhere WSGI File

1. Go to your PythonAnywhere dashboard
2. Click on "Web" tab
3. Find your web app and click "Edit" next to the WSGI configuration file
4. **Replace ALL content** with this EXACT code:

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

### Step 2: Run the Definitive Fix Script

In your PythonAnywhere console, run:

```bash
cd /home/gryttteamtrak/gryttteamtrack/teamtrack
chmod +x DEFINITIVE_FIX.sh
./DEFINITIVE_FIX.sh
```

### Step 3: Reload Your Web App

1. Go back to your PythonAnywhere dashboard
2. Click on "Web" tab
3. Click "Reload" button for your web app

## What This Fixes

✅ **ModuleNotFoundError**: Correctly sets up Python path to find teamtrack module
✅ **Template errors**: Ensures templates are found in the correct directory
✅ **Database errors**: Runs migrations to create missing tables
✅ **App configuration**: Ensures all apps are properly configured

## Testing

After completing these steps, test these URLs:
- `/` - Should redirect to dashboard
- `/accounts/login/` - Login page
- `/dashboard/member/` - Member dashboard
- `/tasks/` - Tasks page
- `/admin/` - Admin interface

## Admin Access
- **Username**: `admin`
- **Password**: `admin123`
- **URL**: `https://yourdomain.pythonanywhere.com/admin/`

## If Issues Persist

1. Check the error logs in PythonAnywhere dashboard
2. Verify the WSGI file content is EXACTLY as shown above
3. Make sure you've run the DEFINITIVE_FIX.sh script
4. Check that all environment variables are set correctly

## Key Changes Made

- Added both project directory AND parent directory to Python path
- This ensures Django can find the `teamtrack` module
- Fixed all template and database issues
- Created comprehensive deployment script
