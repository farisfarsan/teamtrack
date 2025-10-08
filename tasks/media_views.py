from django.http import HttpResponse, Http404
from django.conf import settings
import os
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(never_cache, name='dispatch')
class MediaFileView(View):
    """Serve media files with proper headers"""
    
    def get(self, request, file_path):
        # Construct the full file path
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        
        # Check if file exists
        if not os.path.exists(full_path):
            raise Http404("File not found")
        
        # Read the file
        try:
            with open(full_path, 'rb') as f:
                file_data = f.read()
        except IOError:
            raise Http404("File not accessible")
        
        # Determine content type
        content_type = 'application/octet-stream'
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            content_type = 'image/png' if file_path.lower().endswith('.png') else 'image/jpeg'
        elif file_path.lower().endswith('.pdf'):
            content_type = 'application/pdf'
        elif file_path.lower().endswith(('.doc', '.docx')):
            content_type = 'application/msword'
        elif file_path.lower().endswith('.txt'):
            content_type = 'text/plain'
        
        # Create response with proper headers
        response = HttpResponse(file_data, content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        response['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
        
        return response
