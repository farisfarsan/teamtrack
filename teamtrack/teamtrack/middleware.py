"""
Robust error handling middleware for TeamTrack
This middleware catches and handles errors gracefully to prevent service downtime
"""
import logging
import traceback
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

class RobustErrorMiddleware:
    """Middleware to handle errors gracefully and prevent service downtime"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception in {request.path}: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Try to return a graceful error response
            return self._handle_error(request, e)
    
    def _handle_error(self, request, error):
        """Handle errors gracefully"""
        try:
            # Log the error with context
            error_context = {
                'path': request.path,
                'method': request.method,
                'user': getattr(request, 'user', None),
                'timestamp': timezone.now().isoformat(),
                'error': str(error),
                'traceback': traceback.format_exc()
            }
            
            logger.error(f"Error context: {error_context}")
            
            # Check if this is an API request
            if request.path.startswith('/api/') or 'application/json' in request.META.get('HTTP_ACCEPT', ''):
                return JsonResponse({
                    'error': 'Internal server error',
                    'message': 'Something went wrong. Please try again later.',
                    'timestamp': timezone.now().isoformat(),
                    'status': 'error'
                }, status=500)
            
            # For regular requests, return a simple error page
            return HttpResponse("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Service Temporarily Unavailable</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                    .error-container { max-width: 600px; margin: 0 auto; }
                    .error-code { font-size: 72px; color: #e74c3c; margin: 0; }
                    .error-message { font-size: 24px; color: #2c3e50; margin: 20px 0; }
                    .error-description { font-size: 16px; color: #7f8c8d; margin: 20px 0; }
                    .retry-button { 
                        background: #3498db; color: white; padding: 12px 24px; 
                        border: none; border-radius: 4px; cursor: pointer; 
                        font-size: 16px; margin: 20px 0;
                    }
                    .retry-button:hover { background: #2980b9; }
                </style>
            </head>
            <body>
                <div class="error-container">
                    <h1 class="error-code">500</h1>
                    <h2 class="error-message">Service Temporarily Unavailable</h2>
                    <p class="error-description">
                        We're experiencing some technical difficulties. 
                        Our team has been notified and is working to resolve the issue.
                    </p>
                    <button class="retry-button" onclick="window.location.reload()">
                        Try Again
                    </button>
                    <p style="margin-top: 30px; font-size: 14px; color: #95a5a6;">
                        If the problem persists, please contact support.
                    </p>
                </div>
            </body>
            </html>
            """, status=500)
            
        except Exception as e:
            # If even error handling fails, return a minimal response
            logger.critical(f"Error handling failed: {e}")
            return HttpResponse("Service Unavailable", status=503)


class DatabaseConnectionMiddleware:
    """Middleware to handle database connection issues"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            # Test database connection
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            response = self.get_response(request)
            return response
            
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            
            # Try to recover database connection
            try:
                connection.close()
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                logger.info("Database connection recovered")
                
                # Retry the request
                response = self.get_response(request)
                return response
                
            except Exception as recovery_error:
                logger.error(f"Database recovery failed: {recovery_error}")
                
                # Return error response
                return JsonResponse({
                    'error': 'Database connection failed',
                    'message': 'Please try again in a few moments',
                    'timestamp': timezone.now().isoformat()
                }, status=503)


class CacheRecoveryMiddleware:
    """Middleware to handle cache issues"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            # Test cache
            test_key = f"middleware_test_{int(timezone.now().timestamp())}"
            cache.set(test_key, "test", 10)
            cache.get(test_key)
            cache.delete(test_key)
            
            response = self.get_response(request)
            return response
            
        except Exception as e:
            logger.warning(f"Cache error detected: {e}")
            
            # Try to recover cache
            try:
                cache.clear()
                logger.info("Cache cleared and recovered")
                
                response = self.get_response(request)
                return response
                
            except Exception as recovery_error:
                logger.error(f"Cache recovery failed: {recovery_error}")
                
                # Continue without cache
                response = self.get_response(request)
                return response
