"""
Complete PythonAnywhere WSGI Configuration
Copy this entire content to your PythonAnywhere WSGI file
"""

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
