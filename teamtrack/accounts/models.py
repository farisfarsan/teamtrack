from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from core.constants import TEAMS

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email: raise ValueError("Email required")
        user = self.model(email=self.normalize_email(email), **extra)
        user.set_password(password); user.save(); return user
    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True); extra.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra)

class User(AbstractBaseUser, PermissionsMixin):
    TEAMS = TEAMS
    email = models.EmailField(unique=True)
    name  = models.CharField(max_length=100)
    team  = models.CharField(max_length=20, choices=TEAMS, default="TECH")
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self): return f"{self.name} ({self.get_team_display()})"
    
    @property
    def is_admin(self):
        return self.team == "PROJECT_MANAGER"
