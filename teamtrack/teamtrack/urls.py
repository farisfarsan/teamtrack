from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from .health import health_check
from .keep_alive import keep_alive_ping

def root_redirect(request):
    """Redirect root URL to dashboard"""
    return redirect("dashboard:home")

def favicon_view(request):
    """Handle favicon requests (no actual favicon file)"""
    return HttpResponse(status=204)

urlpatterns = [
    # Health check and keep-alive
    path("health/", health_check, name="health_check"),
    path("keep-alive/", keep_alive_ping, name="keep_alive"),
    
    # Core
    path("", root_redirect, name="root"),
    path("favicon.ico", favicon_view, name="favicon"),
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
