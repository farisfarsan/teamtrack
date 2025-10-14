from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.attendance_list, name="list"),
    path("mark/", views.mark_attendance, name="mark"),
    path("edit/<int:record_id>/", views.edit_attendance, name="edit"),
    path("delete/<int:record_id>/", views.delete_attendance, name="delete"),
]