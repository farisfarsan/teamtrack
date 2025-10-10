from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def root_redirect(request):
    """Redirect root URL to dashboard"""
    return redirect("dashboard:home")

def favicon_view(request):
    """Handle favicon requests (no actual favicon file)"""
    return HttpResponse(status=204)

def keep_alive_view(request):
    """Keep-alive endpoint for external monitoring services"""
    return HttpResponse("OK", status=200)

urlpatterns = [
    # Core
    path("", root_redirect, name="root"),
    path("favicon.ico", favicon_view, name="favicon"),
    path("keep-alive/", keep_alive_view, name="keep_alive"),
    path("admin/", admin.site.urls),

    # Apps (each must have app_name defined in its urls.py)
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("tasks/", include(("tasks.urls", "tasks"), namespace="tasks")),
    path("notifications/", include(("notifications.urls", "notifications"), namespace="notifications")),
    path("meetings/", include(("meetings.urls", "meetings"), namespace="meetings")),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
    path("attendance/", include(("attendance.urls", "attendance"), namespace="attendance")),
]

# Serve media files in development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
