from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import os

@csrf_exempt
def health_check(request):
    """Simple health check endpoint"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'environment': os.getenv('DJANGO_SETTINGS_MODULE', 'not_set'),
            'debug': os.getenv('DEBUG', 'False'),
            'allowed_hosts': os.getenv('ALLOWED_HOSTS', 'not_set')
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'environment': os.getenv('DJANGO_SETTINGS_MODULE', 'not_set')
        }, status=500)
