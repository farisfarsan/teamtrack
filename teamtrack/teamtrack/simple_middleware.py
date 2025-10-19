"""
Simple error handling middleware for TeamTrack
This middleware provides basic error handling without complex dependencies
"""
import logging
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

logger = logging.getLogger(__name__)

class SimpleErrorMiddleware:
    """Simple middleware to handle errors gracefully"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f"Error in {request.path}: {e}")
            
            # Return a simple error response
            if request.path.startswith('/api/') or 'application/json' in request.META.get('HTTP_ACCEPT', ''):
                return JsonResponse({
                    'error': 'Service temporarily unavailable',
                    'message': 'Please try again in a few moments',
                    'timestamp': timezone.now().isoformat()
                }, status=503)
            
            # For regular requests, return a simple error page
            return HttpResponse("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Service Temporarily Unavailable</title>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                    .error-code { font-size: 72px; color: #e74c3c; margin: 0; }
                    .error-message { font-size: 24px; color: #2c3e50; margin: 20px 0; }
                    .retry-button { 
                        background: #3498db; color: white; padding: 12px 24px; 
                        border: none; border-radius: 4px; cursor: pointer; 
                        font-size: 16px; margin: 20px 0;
                    }
                </style>
            </head>
            <body>
                <h1 class="error-code">503</h1>
                <h2 class="error-message">Service Temporarily Unavailable</h2>
                <p>We're experiencing technical difficulties. Please try again in a few moments.</p>
                <button class="retry-button" onclick="window.location.reload()">Try Again</button>
            </body>
            </html>
            """, status=503)
