"""
WSGI config for teamtrack project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use PythonAnywhere settings for production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teamtrack.settings_pythonanywhere")

application = get_wsgi_application()
