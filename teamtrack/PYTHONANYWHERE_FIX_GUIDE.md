# PythonAnywhere Deployment Fix Guide

## Issues Fixed

### 1. ModuleNotFoundError: No module named 'gryttteamtrack.settings'
**Problem**: WSGI configuration was pointing to wrong settings module
**Solution**: Updated WSGI to use `teamtrack.settings_pythonanywhere`

### 2. RuntimeError: Model class attendance.models.AttendanceRecord doesn't declare an explicit app_label
**Problem**: Django couldn't identify which app the model belongs to
**Solution**: Added explicit `app_label = 'attendance'` to the model's Meta class

### 3. TemplateDoesNotExist errors
**Problem**: Template paths were incorrectly configured
**Solution**: Fixed template directory configuration in settings

### 4. MySQL table errors - attendance_attendancerecord table doesn't exist
**Problem**: Database migrations weren't run properly
**Solution**: Created setup script and management command

## Files Modified

1. `teamtrack/wsgi.py` - Updated to use PythonAnywhere settings
2. `teamtrack/attendance/models.py` - Added explicit app_label
3. `teamtrack/settings_pythonanywhere.py` - Fixed template paths
4. `teamtrack/attendance/management/commands/setup_attendance.py` - New management command
5. `teamtrack/fix_pythonanywhere_deployment.sh` - Deployment script
6. `teamtrack/pythonanywhere_wsgi.py` - Complete WSGI configuration

## Deployment Steps

### Step 1: Update PythonAnywhere WSGI File
Replace your PythonAnywhere WSGI file content with the content from `pythonanywhere_wsgi.py`

### Step 2: Run Deployment Script
```bash
cd /home/gryttteamtrak/gryttteamtrack/teamtrack
chmod +x fix_pythonanywhere_deployment.sh
./fix_pythonanywhere_deployment.sh
```

### Step 3: Manual Commands (if script fails)
```bash
# Activate virtual environment
source venv/bin/activate

# Set environment
export DJANGO_SETTINGS_MODULE=teamtrack.settings_pythonanywhere

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Set up attendance
python manage.py setup_attendance

# Collect static files
python manage.py collectstatic --noinput

# Create admin user
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
```

### Step 4: Reload Web App
In PythonAnywhere dashboard, click "Reload" for your web app

## Testing

After deployment, test these URLs:
- `/` - Should redirect to dashboard
- `/accounts/login/` - Login page
- `/dashboard/member/` - Member dashboard
- `/tasks/` - Tasks page
- `/admin/` - Admin interface

## Admin Access
- Username: `admin`
- Password: `admin123`
- URL: `https://yourdomain.pythonanywhere.com/admin/`

## Environment Variables

Make sure these are set in PythonAnywhere:
- `DB_NAME`: Your MySQL database name
- `DB_USER`: Your MySQL username  
- `DB_PASSWORD`: Your MySQL password
- `DB_HOST`: Your MySQL host (usually `yourusername.mysql.pythonanywhere.com`)
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` for production

## Common Issues

### Database Connection Issues
- Verify MySQL database credentials
- Check if database exists in PythonAnywhere MySQL console
- Ensure database user has proper permissions

### Static Files Issues
- Run `python manage.py collectstatic --noinput`
- Check static files URL configuration
- Verify WhiteNoise middleware is enabled

### Template Issues
- Verify template directories in settings
- Check if templates exist in correct locations
- Ensure APP_DIRS is True in template configuration

## Support

If issues persist:
1. Check PythonAnywhere error logs
2. Run `python manage.py check --deploy`
3. Verify all environment variables are set
4. Check database connectivity
5. Review Django logs for specific errors
