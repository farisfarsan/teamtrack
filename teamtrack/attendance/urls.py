from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.attendance_list, name="list"),
    path("mark/", views.mark_attendance, name="mark"),
    path("create/", views.create_record, name="create"),
    path("<int:pk>/edit/", views.edit_record, name="edit"),
    path("<int:pk>/delete/", views.delete_record, name="delete"),
    path("stats/", views.attendance_stats, name="stats"),
]
