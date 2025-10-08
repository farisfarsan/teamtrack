from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.attendance_list, name="list"),
    path("create/", views.create_session, name="create"),
    path("<int:pk>/", views.session_detail, name="detail"),
    path("<int:pk>/mark/", views.mark_attendance, name="mark"),
    path("stats/", views.attendance_stats, name="stats"),
]
