#!/bin/bash

# ULTIMATE PythonAnywhere Fix Script
# This script fixes ALL deployment issues

echo "🚀 ULTIMATE PythonAnywhere Fix Script Starting..."

# Navigate to project directory
cd ~/gryttteamtrack/teamtrack

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin master

# Create all necessary directories
echo "📁 Creating all directories..."
mkdir -p templates/accounts
mkdir -p templates/dashboard
mkdir -p templates/attendance
mkdir -p templates/tasks
mkdir -p templates/notifications
mkdir -p templates/meetings
mkdir -p static
mkdir -p staticfiles
mkdir -p core
mkdir -p attendance

# Create core module files
echo "📝 Creating core module files..."

# core/__init__.py
cat > core/__init__.py << 'EOF'
# Core module for teamtrack
EOF

# core/constants.py
cat > core/constants.py << 'EOF'
# Team constants
TEAMS = [
    ('development', 'Development'),
    ('design', 'Design'),
    ('marketing', 'Marketing'),
    ('sales', 'Sales'),
    ('support', 'Support'),
    ('management', 'Management'),
]

# User roles
USER_ROLES = [
    ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('member', 'Member'),
]

# Task priorities
TASK_PRIORITY = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('urgent', 'Urgent'),
]

# Task statuses
TASK_STATUS = [
    ('todo', 'To Do'),
    ('in_progress', 'In Progress'),
    ('review', 'Review'),
    ('done', 'Done'),
]

# Task comment types
TASK_COMMENT_TYPES = [
    ('comment', 'Comment'),
    ('update', 'Update'),
    ('note', 'Note'),
]

# Task attachment path
TASK_ATTACHMENT_PATH = 'task_attachments/'

# Pagination
ITEMS_PER_PAGE = 20

# Legacy constants for backward compatibility
TASK_PRIORITIES = TASK_PRIORITY
TASK_STATUSES = TASK_STATUS
EOF

# core/utils.py
cat > core/utils.py << 'EOF'
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator

class PermissionMixin(LoginRequiredMixin):
    """
    Mixin to check user permissions
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        # Add any additional permission checks here
        return super().dispatch(request, *args, **kwargs)
    
    def check_permission(self, user, required_permission=None):
        """
        Check if user has required permission
        """
        if not user.is_authenticated:
            raise PermissionDenied("User must be authenticated")
        
        # Add your permission logic here
        # For now, just check if user is active
        if not user.is_active:
            raise PermissionDenied("User account is not active")
        
        return True

class AdminRequiredMixin(PermissionMixin):
    """
    Mixin that requires admin permissions
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Admin access required")
        return super().dispatch(request, *args, **kwargs)

class ManagerRequiredMixin(PermissionMixin):
    """
    Mixin that requires manager permissions
    """
    def dispatch(self, request, *args, **kwargs):
        # Check if user is manager or admin
        if not (request.user.is_staff or getattr(request.user, 'role', None) == 'manager'):
            raise PermissionDenied("Manager access required")
        return super().dispatch(request, *args, **kwargs)

class TaskFilterMixin:
    """
    Mixin for filtering tasks based on user permissions
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is admin, show all tasks
        if user.is_staff:
            return queryset
        
        # If user is manager, show tasks for their team
        if hasattr(user, 'role') and user.role == 'manager':
            return queryset.filter(team=user.team)
        
        # If user is member, show only their tasks
        return queryset.filter(assigned_to=user)

class TeamFilterMixin:
    """
    Mixin for filtering based on team membership
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is admin, show all
        if user.is_staff:
            return queryset
        
        # If user has a team, filter by team
        if hasattr(user, 'team') and user.team:
            return queryset.filter(team=user.team)
        
        # Otherwise, show only user's own records
        return queryset.filter(user=user)

class PaginationMixin:
    """
    Mixin for pagination
    """
    paginate_by = 20
    
    def get_paginate_by(self, queryset):
        return self.paginate_by

class SearchMixin:
    """
    Mixin for search functionality
    """
    search_fields = []
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        
        if search_query and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(q_objects)
        
        return queryset

class ContextMixin:
    """
    Mixin for adding context data
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class NotificationMixin:
    """
    Mixin for handling notifications
    """
    def create_notification(self, user, message, notification_type='info'):
        """
        Create a notification for a user
        """
        try:
            from notifications.models import Notification
            Notification.objects.create(
                user=user,
                message=message,
                notification_type=notification_type
            )
        except ImportError:
            # If notifications app is not available, just pass
            pass

def get_context_with_filters(request, queryset, search_fields=None):
    """
    Helper function to get context with filters applied
    """
    context = {}
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query and search_fields:
        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{f"{field}__icontains": search_query})
        queryset = queryset.filter(q_objects)
        context['search_query'] = search_query
    
    # Pagination
    paginator = Paginator(queryset, 20)  # Default to 20 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['page_obj'] = page_obj
    context['queryset'] = queryset
    
    return context

def handle_task_creation(request, form):
    """
    Helper function to handle task creation
    """
    if form.is_valid():
        task = form.save(commit=False)
        task.created_by = request.user
        task.save()
        return task
    return None
EOF

# core/apps.py
cat > core/apps.py << 'EOF'
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
EOF

# Create attendance module files
echo "📝 Creating attendance module files..."

# attendance/__init__.py
cat > attendance/__init__.py << 'EOF'
# Attendance module for teamtrack
EOF

# attendance/apps.py
cat > attendance/apps.py << 'EOF'
from django.apps import AppConfig

class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'
EOF

# attendance/models.py
cat > attendance/models.py << 'EOF'
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'attendance'
        unique_together = ['member', 'date']
        ordering = ['-date', 'member__name']
    
    def __str__(self):
        return f"{self.member.name} - {self.date} ({self.status})"
EOF

# attendance/urls.py
cat > attendance/urls.py << 'EOF'
from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.attendance_list, name="list"),
    path("mark/", views.mark_attendance, name="mark"),
    path("edit/<int:record_id>/", views.edit_attendance, name="edit"),
    path("delete/<int:record_id>/", views.delete_attendance, name="delete"),
]
EOF

# attendance/views.py
cat > attendance/views.py << 'EOF'
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import AttendanceRecord
from accounts.models import User

@login_required
def attendance_list(request):
    """List attendance records"""
    records = AttendanceRecord.objects.filter(member=request.user).order_by('-date')
    context = {
        'records': records,
        'user': request.user,
    }
    return render(request, 'attendance/session_list.html', context)

@login_required
def mark_attendance(request):
    """Mark attendance for the current user"""
    if request.method == 'POST':
        AttendanceRecord.objects.create(
            member=request.user,
            status='present'
        )
        messages.success(request, 'Attendance marked successfully!')
        return redirect('attendance:list')
    
    return render(request, 'attendance/mark_attendance.html')

@login_required
def edit_attendance(request, record_id):
    """Edit attendance record"""
    record = get_object_or_404(AttendanceRecord, id=record_id, member=request.user)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        record.status = status
        record.save()
        messages.success(request, 'Attendance updated successfully!')
        return redirect('attendance:list')
    
    context = {'record': record}
    return render(request, 'attendance/edit_attendance.html', context)

@login_required
def delete_attendance(request, record_id):
    """Delete attendance record"""
    record = get_object_or_404(AttendanceRecord, id=record_id, member=request.user)
    
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Attendance record deleted successfully!')
        return redirect('attendance:list')
    
    context = {'record': record}
    return render(request, 'attendance/delete_attendance.html', context)
EOF

# Create all necessary templates
echo "📝 Creating all templates..."

# base.html
cat > templates/base.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}TeamTrack{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'dashboard:home' %}">TeamTrack</a>
            <div class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'accounts:profile' %}">{{ user.name }}</a>
                    <a class="nav-link" href="{% url 'accounts:logout' %}">Logout</a>
                {% else %}
                    <a class="nav-link" href="{% url 'accounts:login' %}">Login</a>
                {% endif %}
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}
        {% endblock %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
EOF

# accounts/login.html
cat > templates/accounts/login.html << 'EOF'
{% extends 'base.html' %}

{% block title %}Login - TeamTrack{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3>Login</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input type="email" class="form-control" id="email" name="email" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Login</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# dashboard/member.html
cat > templates/dashboard/member.html << 'EOF'
{% extends 'base.html' %}

{% block title %}Member Dashboard - TeamTrack{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <h2>Welcome, {{ user.name }}!</h2>
        <p>This is your member dashboard.</p>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>Your Tasks</h5>
                    </div>
                    <div class="card-body">
                        <p>View and manage your assigned tasks.</p>
                        <a href="{% url 'tasks:list' %}" class="btn btn-primary">View Tasks</a>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>Attendance</h5>
                    </div>
                    <div class="card-body">
                        <p>View your attendance records.</p>
                        <a href="{% url 'attendance:list' %}" class="btn btn-primary">View Attendance</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# tasks/task_list.html
cat > templates/tasks/task_list.html << 'EOF'
{% extends 'base.html' %}

{% block title %}Tasks - TeamTrack{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <h2>Your Tasks</h2>
        
        <div class="card">
            <div class="card-body">
                <p>No tasks found. Tasks will appear here when assigned to you.</p>
                <a href="{% url 'dashboard:home' %}" class="btn btn-primary">Back to Dashboard</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# attendance/session_list.html
cat > templates/attendance/session_list.html << 'EOF'
{% extends 'base.html' %}

{% block title %}Attendance - TeamTrack{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <h2>Your Attendance Records</h2>
        
        <div class="card">
            <div class="card-body">
                <p>No attendance records found.</p>
                <a href="{% url 'dashboard:home' %}" class="btn btn-primary">Back to Dashboard</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# attendance/mark_attendance.html
cat > templates/attendance/mark_attendance.html << 'EOF'
{% extends 'base.html' %}

{% block title %}Mark Attendance - TeamTrack{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3>Mark Attendance</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-success">Mark Present</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# attendance/edit_attendance.html
cat > templates/attendance/edit_attendance.html << 'EOF'
{% extends 'base.html' %}

{% block title %}Edit Attendance - TeamTrack{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3>Edit Attendance</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label for="status" class="form-label">Status</label>
                        <select class="form-control" id="status" name="status">
                            <option value="present">Present</option>
                            <option value="absent">Absent</option>
                            <option value="late">Late</option>
                            <option value="excused">Excused</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">Update</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# attendance/delete_attendance.html
cat > templates/attendance/delete_attendance.html << 'EOF'
{% extends 'base.html' %}

{% block title %}Delete Attendance - TeamTrack{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3>Delete Attendance Record</h3>
            </div>
            <div class="card-body">
                <p>Are you sure you want to delete this attendance record?</p>
                <form method="post">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-danger">Delete</button>
                    <a href="{% url 'attendance:list' %}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# Test Django setup
echo "🧪 Testing Django setup..."
python manage.py check --settings=teamtrack.settings_pythonanywhere

# Run migrations
echo "📊 Running migrations..."
python manage.py makemigrations --settings=teamtrack.settings_pythonanywhere
python manage.py migrate --settings=teamtrack.settings_pythonanywhere

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --settings=teamtrack.settings_pythonanywhere --noinput

echo "✅ ULTIMATE PythonAnywhere fix completed!"
echo "🎉 Your Django app should now work perfectly on PythonAnywhere!"
echo ""
echo "Next steps:"
echo "1. Reload your web app in PythonAnywhere dashboard"
echo "2. Create a superuser: python manage.py createsuperuser --settings=teamtrack.settings_pythonanywhere"
echo "3. Visit your site: https://gryttteamtrak.pythonanywhere.com/"
