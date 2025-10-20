# PythonAnywhere Deployment Guide for TeamTrack

This guide will help you deploy your Django TeamTrack application to PythonAnywhere.

## Prerequisites

1. **PythonAnywhere Account**: Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)

## Step 1: Prepare Your Code

### 1.1 Create Production Settings
Create a production settings file for PythonAnywhere:

```bash
# In your local project directory
cp teamtrack/settings.py teamtrack/settings_production.py
```

### 1.2 Update Production Settings
Edit `teamtrack/settings_production.py` and make these changes:

```python
# Add these imports at the top
import os
from .settings import *

# Override production-specific settings
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'www.yourusername.pythonanywhere.com']

# Use PythonAnywhere's MySQL database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yourusername$teamtrack',
        'USER': 'yourusername',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'yourusername.mysql.pythonanywhere.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static files configuration for PythonAnywhere
STATIC_URL = '/static/'
STATIC_ROOT = '/home/yourusername/teamtrack/staticfiles/'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/yourusername/teamtrack/media/'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/yourusername/teamtrack/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### 1.3 Create Environment File
Create a `.env` file for production secrets:

```bash
# .env file for production
SECRET_KEY=your-super-secret-key-here
DEBUG=False
DATABASE_URL=mysql://yourusername:yourpassword@yourusername.mysql.pythonanywhere.com/yourusername$teamtrack
```

### 1.4 Update WSGI Configuration
Create `teamtrack/wsgi_production.py`:

```python
import os
import sys

# Add your project directory to the Python path
path = '/home/yourusername/teamtrack'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teamtrack.settings_production")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Step 2: Deploy to PythonAnywhere

### 2.1 Upload Your Code
1. **Option A - Git Clone (Recommended)**:
   ```bash
   # In PythonAnywhere console
   cd ~
   git clone https://github.com/yourusername/your-repo.git teamtrack
   cd teamtrack
   ```

   **Option B - Upload Files**:
   - Use PythonAnywhere's Files tab to upload your project files
   - Or use the Upload a file feature

### 2.2 Set Up Virtual Environment
```bash
# In PythonAnywhere console
cd ~/teamtrack
python3.10 -m venv teamtrack_env
source teamtrack_env/bin/activate
```

### 2.3 Install Dependencies
```bash
# Make sure you're in the virtual environment
pip install --user -r requirements.txt
```

### 2.4 Set Up Database
1. **Create MySQL Database**:
   - Go to PythonAnywhere Dashboard → Databases tab
   - Create a new MySQL database named `teamtrack`
   - Note down the database credentials

2. **Run Migrations**:
   ```bash
   cd ~/teamtrack
   source teamtrack_env/bin/activate
   python manage.py migrate --settings=teamtrack.settings_production
   ```

3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser --settings=teamtrack.settings_production
   ```

### 2.5 Collect Static Files
```bash
python manage.py collectstatic --settings=teamtrack.settings_production --noinput
```

### 2.6 Set Up Environment Variables
Create the `.env` file in your project directory:
```bash
nano ~/teamtrack/.env
```

Add your production environment variables:
```
SECRET_KEY=your-super-secret-key-here
DEBUG=False
DATABASE_URL=mysql://yourusername:yourpassword@yourusername.mysql.pythonanywhere.com/yourusername$teamtrack
```

## Step 3: Configure Web App

### 3.1 Create Web App
1. Go to PythonAnywhere Dashboard → Web tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10

### 3.2 Configure WSGI File
1. In the Web tab, click on your web app
2. Go to the "Code" section
3. Edit the WSGI configuration file
4. Replace the content with:

```python
# This file contains the WSGI configuration required to serve up your
# web application at http://yourusername.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.

import os
import sys

# add your project directory to the sys.path
project_home = '/home/yourusername/teamtrack'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'teamtrack.settings_production'

# serve django application via wsgi
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 3.3 Configure Static Files
1. In the Web tab, go to "Static files" section
2. Add these mappings:
   - **URL**: `/static/`
   - **Directory**: `/home/yourusername/teamtrack/staticfiles/`
   - **URL**: `/media/`
   - **Directory**: `/home/yourusername/teamtrack/media/`

### 3.4 Configure Domain
1. In the Web tab, go to "Domains" section
2. Add your domain: `yourusername.pythonanywhere.com`

## Step 4: Final Configuration

### 4.1 Create Required Directories
```bash
mkdir -p ~/teamtrack/logs
mkdir -p ~/teamtrack/media
mkdir -p ~/teamtrack/staticfiles
```

### 4.2 Set Permissions
```bash
chmod 755 ~/teamtrack
chmod 755 ~/teamtrack/logs
chmod 755 ~/teamtrack/media
chmod 755 ~/teamtrack/staticfiles
```

### 4.3 Test Your Application
1. Go to your web app URL: `https://yourusername.pythonanywhere.com`
2. Test the admin interface: `https://yourusername.pythonanywhere.com/admin/`
3. Test the health endpoint: `https://yourusername.pythonanywhere.com/health/`

## Step 5: Production Optimizations

### 5.1 Set Up Scheduled Tasks (Optional)
If you have management commands that need to run periodically:

1. Go to PythonAnywhere Dashboard → Tasks tab
2. Create scheduled tasks for:
   - `python ~/teamtrack/manage.py send_attendance_reminders --settings=teamtrack.settings_production`
   - `python ~/teamtrack/manage.py cleanup_fake_users --settings=teamtrack.settings_production`

### 5.2 Set Up Monitoring
1. Use the health endpoint: `/health/`
2. Monitor logs in `/home/yourusername/teamtrack/logs/django.log`
3. Set up uptime monitoring with external services

## Troubleshooting

### Common Issues:

1. **Import Errors**:
   - Make sure your virtual environment is activated
   - Check that all dependencies are installed
   - Verify Python path in WSGI file

2. **Database Connection Issues**:
   - Verify database credentials
   - Check MySQL database exists
   - Ensure database user has proper permissions

3. **Static Files Not Loading**:
   - Run `collectstatic` command
   - Check static files mapping in Web tab
   - Verify file permissions

4. **Permission Errors**:
   - Check file and directory permissions
   - Ensure PythonAnywhere user owns the files

### Useful Commands:

```bash
# Check logs
tail -f ~/teamtrack/logs/django.log

# Restart web app
# Go to Web tab and click "Reload"

# Check database connection
python manage.py dbshell --settings=teamtrack.settings_production

# Run tests
python manage.py test --settings=teamtrack.settings_production
```

## Security Checklist

- [ ] DEBUG = False in production settings
- [ ] Strong SECRET_KEY
- [ ] HTTPS enabled
- [ ] Secure cookies enabled
- [ ] Database credentials secured
- [ ] Static files properly configured
- [ ] Error logging enabled
- [ ] CSRF protection enabled

## Next Steps

1. **Domain Setup**: Configure custom domain if needed
2. **SSL Certificate**: PythonAnywhere provides free SSL
3. **Backup Strategy**: Set up regular database backups
4. **Monitoring**: Implement application monitoring
5. **Performance**: Optimize database queries and caching

Your TeamTrack application should now be live at `https://yourusername.pythonanywhere.com`!

## Support

If you encounter issues:
1. Check PythonAnywhere's documentation
2. Review Django deployment documentation
3. Check the error logs in your project
4. Contact PythonAnywhere support if needed
