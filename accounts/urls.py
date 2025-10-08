from django.urls import path
from .views import login_view, logout_view, profile_view, profile_update
app_name = "accounts"
urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/update/", profile_update, name="profile_update"),
]
