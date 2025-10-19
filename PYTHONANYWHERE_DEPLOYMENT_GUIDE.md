# PythonAnywhere Deployment Guide

## 🚀 Complete Step-by-Step Migration from Render to PythonAnywhere

### Prerequisites
- PythonAnywhere account (free tier)
- Your Django project ready for deployment

---

## Step 1: Create PythonAnywhere Account

1. **Sign up**: Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. **Choose free tier**: Select "Beginner" plan (100% free)
3. **Verify email**: Complete email verification

---

## Step 2: Upload Your Code

### Option A: Git Clone (Recommended)
```bash
# In PythonAnywhere console
git clone https://github.com/farisfarsan/teamtrack.git
cd teamtrack
```

### Option B: Upload Files
1. Go to **Files** tab in PythonAnywhere dashboard
2. Navigate to `/home/yourusername/`
3. Upload your project files

---

## Step 3: Set Up Virtual Environment

```bash
# In PythonAnywhere console
cd teamtrack
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Step 4: Configure Database

1. **Go to Databases tab** in PythonAnywhere dashboard
2. **Create MySQL database**:
   - Database name: `yourusername$teamtrack`
   - Password: Choose a strong password
3. **Note down credentials**:
   - Host: `yourusername.mysql.pythonanywhere.com`
   - Username: `yourusername`
   - Database: `yourusername$teamtrack`

---

## Step 5: Configure Environment Variables

Create `.env` file in your project root:
```bash
# In PythonAnywhere console
nano .env
```

Add these variables:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
DB_NAME=yourusername$teamtrack
DB_USER=yourusername
DB_PASSWORD=your-database-password
DB_HOST=yourusername.mysql.pythonanywhere.com
DB_PORT=3306
```

---

## Step 6: Run Migrations

```bash
# In PythonAnywhere console
source venv/bin/activate
cd teamtrack
python manage.py migrate --settings=teamtrack.settings_pythonanywhere
```

---

## Step 7: Create Superuser

```bash
python manage.py createsuperuser --settings=teamtrack.settings_pythonanywhere
```

---

## Step 8: Collect Static Files

```bash
python manage.py collectstatic --noinput --settings=teamtrack.settings_pythonanywhere
```

---

## Step 9: Set Up Web App

1. **Go to Web tab** in PythonAnywhere dashboard
2. **Click "Add a new web app"**
3. **Choose "Manual configuration"**
4. **Select Python 3.10**
5. **Configure WSGI file**:

Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import os
import sys

# Add your project directory to the Python path
path = '/home/yourusername/teamtrack'
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'teamtrack.settings_pythonanywhere'

# Activate virtual environment
activate_this = '/home/yourusername/teamtrack/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## Step 10: Configure Static Files

1. **Go to Web tab**
2. **Click on your web app**
3. **Go to Static files section**
4. **Add static file mapping**:
   - URL: `/static/`
   - Directory: `/home/yourusername/teamtrack/staticfiles`

---

## Step 11: Create Users

```bash
# In PythonAnywhere console
source venv/bin/activate
cd teamtrack
python manage.py setup_users --settings=teamtrack.settings_pythonanywhere
```

---

## Step 12: Test Your App

1. **Go to Web tab**
2. **Click "Reload"** button
3. **Visit your app**: `https://yourusername.pythonanywhere.com`

---

## Step 13: Set Up Custom Domain (Optional)

1. **Go to Web tab**
2. **Click "Add a new domain"**
3. **Enter your domain**
4. **Update DNS settings** as instructed

---

## 🔧 Troubleshooting

### Common Issues:

1. **Import Error**: Check virtual environment is activated
2. **Database Error**: Verify database credentials
3. **Static Files**: Ensure static files are collected
4. **Permission Error**: Check file permissions

### Debug Commands:
```bash
# Check Django configuration
python manage.py check --settings=teamtrack.settings_pythonanywhere

# Test database connection
python manage.py dbshell --settings=teamtrack.settings_pythonanywhere

# Check static files
python manage.py findstatic admin/css/base.css --settings=teamtrack.settings_pythonanywhere
```

---

## 🎉 Benefits of PythonAnywhere

✅ **100% Free** - No credit card required  
✅ **No Sleep Issues** - Always running  
✅ **Django Optimized** - Built for Python apps  
✅ **MySQL Database** - Included in free tier  
✅ **Easy Deployment** - Simple setup process  
✅ **Custom Domain** - Available  
✅ **Reliable** - No 503 errors  

---

## 📞 Support

- PythonAnywhere Help: [help.pythonanywhere.com](https://help.pythonanywhere.com)
- Django Documentation: [docs.djangoproject.com](https://docs.djangoproject.com)

Your Django app is now running on PythonAnywhere with no sleep issues! 🚀
