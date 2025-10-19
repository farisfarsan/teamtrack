from .settings import *

# PythonAnywhere specific settings
DEBUG = False

# PythonAnywhere domains
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.pythonanywhere.com',  # PythonAnywhere domain
]

# CSRF settings for PythonAnywhere
CSRF_TRUSTED_ORIGINS = [
    'https://*.pythonanywhere.com',
]

# Use SQLite database (PythonAnywhere free tier)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/yourusername/teamtrack_db.sqlite3',
    }
}

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = '/home/yourusername/teamtrack/staticfiles'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/yourusername/teamtrack/media'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Session settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging for PythonAnywhere
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
