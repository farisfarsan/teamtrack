# PythonAnywhere WSGI Configuration
# Replace 'yourusername' with your actual PythonAnywhere username

import os
import sys

# Add your project directory to Python path
path = '/home/yourusername/teamtrack'
if path not in sys.path:
    sys.path.append(path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'teamtrack.settings_pythonanywhere'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
