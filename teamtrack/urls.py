from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.utils import timezone

def root_redirect(request):
    """Redirect root URL to dashboard"""
    return redirect("dashboard:home")

def favicon_view(request):
    """Handle favicon requests (no actual favicon file)"""
    return HttpResponse(status=204)

def keep_alive_view(request):
    """Simple keep-alive endpoint for external monitoring services"""
    from teamtrack.simple_health import simple_keep_alive
    return simple_keep_alive(request)

def health_view(request):
    """Health check endpoint for PythonAnywhere"""
    from teamtrack.health import health_check
    return health_check(request)

def recovery_view(request):
    """Manual recovery endpoint for testing"""
    from teamtrack.task_manager import TaskManager
    from django.http import JsonResponse
    
    try:
        success, message = TaskManager.restore_all_tasks()
        return JsonResponse({
            'success': success,
            'message': message,
            'timestamp': timezone.now().isoformat()
        }, status=200 if success else 500)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Recovery error: {str(e)}',
            'timestamp': timezone.now().isoformat()
        }, status=500)

urlpatterns = [
    # Core
    path("", root_redirect, name="root"),
    path("favicon.ico", favicon_view, name="favicon"),
    path("keep-alive/", keep_alive_view, name="keep_alive"),
    path("health/", health_view, name="health"),
    path("recovery/", recovery_view, name="recovery"),
    path("admin/", admin.site.urls),

    # Apps (each must have app_name defined in its urls.py)
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("tasks/", include(("tasks.urls", "tasks"), namespace="tasks")),
    path("notifications/", include(("notifications.urls", "notifications"), namespace="notifications")),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
    path("attendance/", include(("attendance.urls", "attendance"), namespace="attendance")),
]

# Serve media files in development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
