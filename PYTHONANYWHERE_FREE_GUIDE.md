# PythonAnywhere Deployment Guide - 100% FREE

## 🐍 PythonAnywhere (Completely Free + Always Online)

PythonAnywhere is **100% free** and keeps your Django app **always online** - no sleep mode!

### ✅ Benefits:
- 🆓 **100% FREE** - No credit card required
- 🌐 **Always online** - No sleep mode like Render
- 🐍 **Django-optimized** - Built for Python apps
- 💾 **500MB storage** - Enough for your app
- ⚡ **100 seconds CPU/day** - Sufficient for small apps
- 🔒 **SSL included** - Secure HTTPS
- 📱 **Custom domain** - Your own domain name

### 🚀 Step-by-Step Setup:

#### 1. Create Account
1. Go to **[PythonAnywhere.com](https://pythonanywhere.com)**
2. Click **"Sign up for free account"**
3. Choose **"Beginner"** account (free)
4. Verify your email

#### 2. Create Web App
1. Go to **"Web"** tab in dashboard
2. Click **"Add a new web app"**
3. Choose **"Django"** framework
4. Select **Python 3.10** (latest)
5. Choose **"Manual configuration"**

#### 3. Upload Your Code
1. Go to **"Files"** tab
2. Navigate to `/home/yourusername/`
3. Open **"Console"** tab
4. Run these commands:

```bash
# Clone your repository
git clone https://github.com/farisfarsan/teamtrack.git

# Navigate to project
cd teamtrack

# Install requirements
pip3.10 install --user -r requirements.txt
```

#### 4. Configure Database
1. Go to **"Databases"** tab
2. Click **"Create database"**
3. Choose **"SQLite"** (free)
4. Name it `teamtrack_db`

#### 5. Configure Web App
1. Go to **"Web"** tab
2. Click on your web app
3. Update **WSGI configuration file**:

```python
import os
import sys

# Add your project directory to Python path
path = '/home/yourusername/teamtrack'
if path not in sys.path:
    sys.path.append(path)

# Set Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'teamtrack.settings_pythonanywhere'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### 6. Create PythonAnywhere Settings
Create `teamtrack/settings_pythonanywhere.py`:

```python
from .settings import *

# PythonAnywhere specific settings
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

# Use SQLite database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/yourusername/teamtrack_db.sqlite3',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = '/home/yourusername/teamtrack/staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/yourusername/teamtrack/media'
```

#### 7. Run Migrations
In **Console** tab:
```bash
cd teamtrack
python3.10 manage.py migrate --settings=teamtrack.settings_pythonanywhere
python3.10 manage.py collectstatic --noinput --settings=teamtrack.settings_pythonanywhere
python3.10 manage.py createsuperuser --settings=teamtrack.settings_pythonanywhere
```

#### 8. Configure Static Files
1. Go to **"Web"** tab
2. Add **Static files mapping**:
   - **URL**: `/static/`
   - **Directory**: `/home/yourusername/teamtrack/staticfiles`

#### 9. Reload Web App
1. Click **"Reload"** button
2. Your app will be live at: `https://yourusername.pythonanywhere.com`

### 🔧 Troubleshooting:

#### If migrations fail:
```bash
# Check database permissions
ls -la /home/yourusername/
chmod 755 /home/yourusername/teamtrack_db.sqlite3
```

#### If static files don't load:
```bash
# Recollect static files
python3.10 manage.py collectstatic --noinput --settings=teamtrack.settings_pythonanywhere
```

#### If app doesn't start:
- Check **"Error log"** in Web tab
- Verify WSGI configuration
- Check Python path in WSGI file

### 📊 PythonAnywhere Limits (Free Tier):
- ✅ **Always online** - No sleep mode
- ✅ **500MB storage** - Plenty for Django app
- ✅ **100 seconds CPU/day** - Sufficient for small apps
- ✅ **1 web app** - Perfect for your project
- ✅ **SSL certificate** - HTTPS included
- ✅ **Custom domain** - Your own domain

### 🎯 Why PythonAnywhere is Perfect:
1. **100% FREE** - No hidden costs
2. **Always online** - Unlike Render's sleep mode
3. **Django-optimized** - Built for Python apps
4. **Easy setup** - No complex configuration
5. **Reliable** - Been around for years

### 🚀 Next Steps:
1. **Sign up** at PythonAnywhere
2. **Follow the setup guide** above
3. **Your app will be always online** and completely free!

---

## Alternative: Fly.io (Also Free)

If you want more control, Fly.io also offers free tier:

1. **Install Fly CLI**
2. **Run `fly launch`**
3. **Configure PostgreSQL**
4. **Deploy with `fly deploy`**

But PythonAnywhere is **easier** and **more reliable** for Django apps.
