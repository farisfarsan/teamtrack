"""
Simple keep-alive endpoint for external monitoring
"""
from django.http import JsonResponse
from django.utils import timezone

def simple_keep_alive(request):
    """
    Simple endpoint that returns current timestamp
    Used by external monitoring services to check if the app is alive
    """
    return JsonResponse({
        'status': 'alive',
        'timestamp': timezone.now().isoformat(),
        'message': 'TeamTrack is running'
    })
