from django.urls import path
from . import views
from .media_views import MediaFileView

app_name = "tasks"

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("create/", views.task_create, name="task_create"),
    path("<int:pk>/", views.task_detail, name="task_detail"),
    path("<int:pk>/update/", views.task_update, name="task_update"),
    path("<int:pk>/delete/", views.task_delete, name="task_delete"),
    path("<int:pk>/status/", views.task_status_update, name="task_status_update"),
    path("<int:pk>/comment/", views.task_add_comment, name="task_add_comment"),
    path("media/<path:file_path>", MediaFileView.as_view(), name="media_file"),
]
