#!/usr/bin/env python3
"""
PythonAnywhere Deployment Troubleshooting Script
Run this script to diagnose and fix deployment issues
"""

import os
import sys
import django
from pathlib import Path

def check_python_path():
    """Check if the project is in Python path"""
    print("🔍 Checking Python path...")
    project_path = "/home/gryttteamtrak/gryttteamtrack/teamtrack"
    if project_path in sys.path:
        print("✅ Project path found in sys.path")
    else:
        print("❌ Project path NOT found in sys.path")
        print(f"Adding {project_path} to sys.path")
        sys.path.insert(0, project_path)
    
    return project_path

def check_settings_module():
    """Check if settings module can be imported"""
    print("\n🔍 Checking settings module...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamtrack.settings_pythonanywhere')
        django.setup()
        print("✅ Django settings loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error loading Django settings: {e}")
        return False

def check_templates():
    """Check if templates exist"""
    print("\n🔍 Checking templates...")
    project_path = Path("/home/gryttteamtrak/gryttteamtrack/teamtrack")
    template_dirs = [
        project_path / "templates",
        project_path / "templates" / "accounts",
        project_path / "templates" / "dashboard", 
        project_path / "templates" / "tasks"
    ]
    
    for template_dir in template_dirs:
        if template_dir.exists():
            print(f"✅ {template_dir} exists")
        else:
            print(f"❌ {template_dir} does not exist")

def check_database():
    """Check database connection and tables"""
    print("\n🔍 Checking database...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"✅ Database connected. Found {len(tables)} tables")
            
            # Check for attendance table
            attendance_tables = [t for t in tables if 'attendance' in str(t).lower()]
            if attendance_tables:
                print(f"✅ Attendance tables found: {attendance_tables}")
            else:
                print("❌ No attendance tables found")
                
    except Exception as e:
        print(f"❌ Database error: {e}")

def check_apps():
    """Check if all apps are properly configured"""
    print("\n🔍 Checking installed apps...")
    try:
        from django.conf import settings
        installed_apps = settings.INSTALLED_APPS
        required_apps = ['accounts', 'attendance', 'dashboard', 'tasks']
        
        for app in required_apps:
            if app in installed_apps:
                print(f"✅ {app} is in INSTALLED_APPS")
            else:
                print(f"❌ {app} is NOT in INSTALLED_APPS")
                
    except Exception as e:
        print(f"❌ Error checking apps: {e}")

def main():
    """Main troubleshooting function"""
    print("🚀 PythonAnywhere Deployment Troubleshooting")
    print("=" * 50)
    
    # Check Python path
    check_python_path()
    
    # Check settings
    if check_settings_module():
        check_templates()
        check_database()
        check_apps()
    
    print("\n" + "=" * 50)
    print("📋 Next Steps:")
    print("1. Update your PythonAnywhere WSGI file with the correct content")
    print("2. Run: python manage.py migrate")
    print("3. Run: python manage.py collectstatic --noinput")
    print("4. Reload your web app in PythonAnywhere dashboard")

if __name__ == "__main__":
    main()
