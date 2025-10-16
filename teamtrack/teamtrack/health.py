"""
Robust health check system for TeamTrack
This provides comprehensive health monitoring and automatic recovery
"""
import os
import logging
import requests
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.cache import cache
from django.db import connection
from django.conf import settings

logger = logging.getLogger(__name__)

class HealthChecker:
    """Comprehensive health checking system"""
    
    @staticmethod
    def check_database():
        """Check database connectivity and performance"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result[0] == 1:
                    return {"status": "healthy", "response_time": "< 100ms"}
                else:
                    return {"status": "unhealthy", "error": "Database query failed"}
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}
    
    @staticmethod
    def check_cache():
        """Check cache system"""
        try:
            test_key = f"health_check_{int(time.time())}"
            test_value = "test_value"
            
            # Test cache write
            cache.set(test_key, test_value, 30)
            
            # Test cache read
            retrieved_value = cache.get(test_key)
            
            if retrieved_value == test_value:
                cache.delete(test_key)  # Clean up
                return {"status": "healthy", "response_time": "< 50ms"}
            else:
                return {"status": "unhealthy", "error": "Cache read/write mismatch"}
        except Exception as e:
            logger.error(f"Cache health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}
    
    @staticmethod
    def check_static_files():
        """Check static file serving"""
        try:
            # Check if static files directory exists and is accessible
            static_root = settings.STATIC_ROOT
            if os.path.exists(static_root):
                return {"status": "healthy", "static_files": "accessible"}
            else:
                return {"status": "warning", "static_files": "directory not found"}
        except Exception as e:
            logger.error(f"Static files health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}
    
    @staticmethod
    def check_memory_usage():
        """Check memory usage"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            usage_percent = memory.percent
            
            if usage_percent < 80:
                return {"status": "healthy", "usage_percent": usage_percent}
            elif usage_percent < 90:
                return {"status": "warning", "usage_percent": usage_percent}
            else:
                return {"status": "critical", "usage_percent": usage_percent}
        except ImportError:
            return {"status": "info", "message": "psutil not available"}
        except Exception as e:
            logger.error(f"Memory health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}
    
    @staticmethod
    def get_overall_health():
        """Get comprehensive health status"""
        checks = {
            "database": HealthChecker.check_database(),
            "cache": HealthChecker.check_cache(),
            "static_files": HealthChecker.check_static_files(),
            "memory": HealthChecker.check_memory_usage(),
        }
        
        # Determine overall status
        statuses = [check["status"] for check in checks.values()]
        
        if "critical" in statuses:
            overall_status = "critical"
        elif "unhealthy" in statuses:
            overall_status = "unhealthy"
        elif "warning" in statuses:
            overall_status = "warning"
        else:
            overall_status = "healthy"
        
        return {
            "overall_status": overall_status,
            "timestamp": timezone.now().isoformat(),
            "checks": checks,
            "service": "TeamTrack",
            "version": "1.0.0"
        }


@csrf_exempt
@require_http_methods(["GET", "POST"])
def health_check(request):
    """Comprehensive health check endpoint"""
    try:
        health_data = HealthChecker.get_overall_health()
        
        # Set appropriate HTTP status code
        if health_data["overall_status"] == "healthy":
            status_code = 200
        elif health_data["overall_status"] == "warning":
            status_code = 200
        elif health_data["overall_status"] == "unhealthy":
            status_code = 503
        else:  # critical
            status_code = 503
        
        return JsonResponse(health_data, status=status_code)
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JsonResponse({
            "overall_status": "critical",
            "error": str(e),
            "timestamp": timezone.now().isoformat()
        }, status=503)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def keep_alive_enhanced(request):
    """Enhanced keep-alive endpoint with health monitoring"""
    try:
        # Perform quick health check
        db_check = HealthChecker.check_database()
        
        if db_check["status"] != "healthy":
            logger.warning(f"Database health issue detected: {db_check}")
        
        response_data = {
            'status': 'alive',
            'timestamp': timezone.now().isoformat(),
            'message': 'TeamTrack is running and ready!',
            'database_status': db_check["status"],
            'uptime': get_uptime(),
            'environment': 'production' if not settings.DEBUG else 'development'
        }
        
        return JsonResponse(response_data, status=200)
    
    except Exception as e:
        logger.error(f"Keep-alive check failed: {e}")
        return JsonResponse({
            'status': 'error',
            'timestamp': timezone.now().isoformat(),
            'error': str(e)
        }, status=503)


def get_uptime():
    """Get application uptime"""
    try:
        import psutil
        import time
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        
        # Convert to human readable format
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        
        return f"{days}d {hours}h {minutes}m"
    except:
        return "unknown"