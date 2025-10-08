from django.urls import path
from . import views
app_name = "dashboard"
urlpatterns = [
    path("", views.home_redirect, name="home"),
    path("admin/", views.admin_dashboard, name="admin"),
    path("manager/", views.manager_dashboard, name="manager"),
    path("member/", views.member_dashboard, name="member"),
]
