from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import HttpResponse

def root_redirect(request):
    """Redirect root URL to dashboard"""
    return redirect("dashboard:home")

def favicon_view(request):
    """Handle favicon requests (no actual favicon file)"""
    return HttpResponse(status=204)

urlpatterns = [
    # Core
    path("", root_redirect, name="root"),
    path("favicon.ico", favicon_view, name="favicon"),
    path("admin/", admin.site.urls),

    # Apps (each must have app_name defined in its urls.py)
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("tasks/", include(("tasks.urls", "tasks"), namespace="tasks")),
    path("notifications/", include(("notifications.urls", "notifications"), namespace="notifications")),
    path("meetings/", include(("meetings.urls", "meetings"), namespace="meetings")),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
]
