"""
WSGI config for teamtrack project - Production Version for PythonAnywhere.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

# Add your project directory to the Python path
path = '/home/yourusername/teamtrack'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teamtrack.settings_production")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
