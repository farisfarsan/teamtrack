# PythonAnywhere Deployment - Complete Step-by-Step Guide

## 🎯 Your PythonAnywhere Setup: gryttteamtrak.pythonanywhere.com

### Step 1: Create Web App
1. Go to **"Web"** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Choose **"Django"** framework
4. Select **Python 3.10**
5. Choose **"Manual configuration"**

### Step 2: Upload Your Code
1. Go to **"Consoles"** tab
2. Click **"$ Bash"** to open console
3. Run these commands:

```bash
# Clone your repository
git clone https://github.com/farisfarsan/teamtrack.git

# Navigate to project
cd teamtrack

# Install requirements
pip3.10 install --user -r requirements.txt

# Check if installation worked
python3.10 -c "import django; print('Django version:', django.get_version())"
```

### Step 3: Configure Database
1. Go to **"Databases"** tab
2. Click **"Create database"**
3. Choose **"SQLite"**
4. Name it: `teamtrack_db`

### Step 4: Update WSGI Configuration
1. Go to **"Web"** tab
2. Click on your web app
3. Find **"WSGI configuration file"** section
4. Replace the content with:

```python
import os
import sys

# Add your project directory to Python path
path = '/home/gryttteamtrak/teamtrack'
if path not in sys.path:
    sys.path.append(path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'teamtrack.settings_pythonanywhere'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 5: Run Django Setup Commands
In Console (Bash):

```bash
cd teamtrack

# Run migrations
python3.10 manage.py migrate --settings=teamtrack.settings_pythonanywhere

# Collect static files
python3.10 manage.py collectstatic --noinput --settings=teamtrack.settings_pythonanywhere

# Create superuser (optional)
python3.10 manage.py createsuperuser --settings=teamtrack.settings_pythonanywhere
```

### Step 6: Configure Static Files
1. Go to **"Web"** tab
2. Scroll down to **"Static files"** section
3. Add this mapping:
   - **URL:** `/static/`
   - **Directory:** `/home/gryttteamtrak/teamtrack/staticfiles`

### Step 7: Configure Media Files (if needed)
1. In **"Static files"** section, also add:
   - **URL:** `/media/`
   - **Directory:** `/home/gryttteamtrak/teamtrack/media`

### Step 8: Reload Web App
1. Click **"Reload"** button in Web tab
2. Your app will be live at: `https://gryttteamtrak.pythonanywhere.com`

## 🔧 Troubleshooting Commands

If something goes wrong, try these in Console:

```bash
# Check if Django is working
cd teamtrack
python3.10 manage.py check --settings=teamtrack.settings_pythonanywhere

# Check database
python3.10 manage.py dbshell --settings=teamtrack.settings_pythonanywhere

# Recollect static files
python3.10 manage.py collectstatic --noinput --settings=teamtrack.settings_pythonanywhere

# Check file permissions
ls -la /home/gryttteamtrak/teamtrack/
```

## 📋 Quick Checklist

- [ ] Web app created (Django, Python 3.10, Manual config)
- [ ] Code cloned from GitHub
- [ ] Requirements installed
- [ ] Database created (SQLite)
- [ ] WSGI file updated
- [ ] Migrations run
- [ ] Static files collected
- [ ] Static files mapping added
- [ ] Web app reloaded

## 🎉 Expected Result

After completing all steps:
- ✅ Your Django app will be live at `https://gryttteamtrak.pythonanywhere.com`
- ✅ Always online (no sleep mode)
- ✅ 100% free hosting
- ✅ SSL certificate included
- ✅ Custom domain ready

## 🆘 If You Get Stuck

1. Check **"Error log"** in Web tab
2. Check **"Server log"** in Web tab
3. Verify all file paths are correct
4. Make sure Python path includes your project directory
5. Contact PythonAnywhere support if needed

Your Django app will be running and always accessible! 🚀
