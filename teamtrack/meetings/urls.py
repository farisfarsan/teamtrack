from django.urls import path
from . import views

app_name = "meetings"

urlpatterns = [
    path("", views.meeting_list, name="list"),
    path("create/", views.create_meeting, name="create"),
    path("<int:pk>/", views.meeting_detail, name="detail"),
    path("<int:pk>/attendance/", views.mark_attendance, name="attendance"),
    path("<int:pk>/manage-attendance/", views.attendance_management, name="manage_attendance"),
    path("attendance-stats/", views.attendance_stats, name="attendance_stats"),
]
