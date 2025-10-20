# PythonAnywhere WSGI Configuration Fix

## The Problem
Your PythonAnywhere WSGI file is still looking for `gryttteamtrack.settings` instead of the correct settings module.

## The Solution

### Step 1: Update Your PythonAnywhere WSGI File

1. Go to your PythonAnywhere dashboard
2. Click on "Web" tab
3. Find your web app and click "Edit" next to the WSGI configuration file
4. **Replace ALL content** with the following:

```python
import os
import sys

# Add your project directory to the Python path
path = '/home/gryttteamtrak/gryttteamtrack/teamtrack'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamtrack.settings_pythonanywhere')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 2: Run the Deployment Script

In your PythonAnywhere console, run:

```bash
cd /home/gryttteamtrak/gryttteamtrack/teamtrack
chmod +x complete_pythonanywhere_fix.sh
./complete_pythonanywhere_fix.sh
```

### Step 3: Reload Your Web App

1. Go back to your PythonAnywhere dashboard
2. Click on "Web" tab
3. Click "Reload" button for your web app

## What This Fixes

1. **ModuleNotFoundError**: Correctly points to the right settings module
2. **Template errors**: Ensures templates are found in the correct directory
3. **Database errors**: Runs migrations to create missing tables
4. **App configuration**: Ensures all apps are properly configured

## Testing

After completing these steps, test these URLs:
- `/` - Should redirect to dashboard
- `/accounts/login/` - Login page
- `/dashboard/member/` - Member dashboard
- `/tasks/` - Tasks page
- `/admin/` - Admin interface

## Admin Access
- Username: `admin`
- Password: `admin123`
- URL: `https://yourdomain.pythonanywhere.com/admin/`

## If Issues Persist

1. Check the error logs in PythonAnywhere dashboard
2. Verify the WSGI file content is exactly as shown above
3. Make sure you've run the deployment script
4. Check that all environment variables are set correctly
