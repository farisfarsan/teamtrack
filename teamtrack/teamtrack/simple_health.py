"""
Simple health check system for TeamTrack
This provides basic health monitoring without complex dependencies
"""
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import connection
from teamtrack.startup_recovery import get_recovery_status

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def simple_health_check(request):
    """Simple health check endpoint"""
    try:
        # Basic database check
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            db_healthy = result[0] == 1
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_healthy = False
    
    # Determine overall status
    if db_healthy:
        status_code = 200
        overall_status = "healthy"
    else:
        status_code = 503
        overall_status = "unhealthy"
    
    # Get recovery status
    recovery_status = get_recovery_status()
    
    response_data = {
        "status": overall_status,
        "timestamp": timezone.now().isoformat(),
        "database": "healthy" if db_healthy else "unhealthy",
        "service": "TeamTrack",
        "message": "Service is running" if db_healthy else "Service has issues",
        "recovery": {
            "attempted": recovery_status['recovery_attempted'],
            "backup_available": recovery_status['backup_info']['has_backup'],
            "backup_task_count": recovery_status['backup_info']['task_count']
        }
    }
    
    return JsonResponse(response_data, status=status_code)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def simple_keep_alive(request):
    """Simple keep-alive endpoint"""
    try:
        # Quick database check
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            db_ok = result[0] == 1
    except Exception as e:
        logger.error(f"Keep-alive database check failed: {e}")
        db_ok = False
    
    if db_ok:
        return JsonResponse({
            'status': 'alive',
            'timestamp': timezone.now().isoformat(),
            'message': 'TeamTrack is running and ready!',
            'database': 'connected'
        }, status=200)
    else:
        return JsonResponse({
            'status': 'error',
            'timestamp': timezone.now().isoformat(),
            'message': 'Database connection issue',
            'database': 'disconnected'
        }, status=503)
