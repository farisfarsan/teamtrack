from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import datetime

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for PythonAnywhere
    Returns basic system status
    """
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Test user model
        from accounts.models import User
        user_count = User.objects.count()
        
        return JsonResponse({
            'status': 'healthy',
            'timestamp': datetime.datetime.now().isoformat(),
            'database': 'connected',
            'users_count': user_count,
            'message': 'TeamTrack is running smoothly on PythonAnywhere!'
        })
    
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'timestamp': datetime.datetime.now().isoformat(),
            'error': str(e),
            'message': 'TeamTrack has an issue'
        }, status=500)
