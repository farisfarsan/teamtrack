#!/bin/bash

# PythonAnywhere Fix Script
# This script ensures all required files are present and correct

echo "🔧 Fixing PythonAnywhere deployment..."

# Navigate to project directory
cd ~/gryttteamtrack/teamtrack

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin master

# Ensure core directory exists
mkdir -p core

# Create core/__init__.py
echo "📝 Creating core/__init__.py..."
cat > core/__init__.py << 'EOF'
# Core module for teamtrack
EOF

# Create core/constants.py
echo "📝 Creating core/constants.py..."
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

# Create core/utils.py
echo "📝 Creating core/utils.py..."
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

# Create core/apps.py
echo "📝 Creating core/apps.py..."
cat > core/apps.py << 'EOF'
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
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

echo "✅ PythonAnywhere deployment fix complete!"
echo "🎉 Your Django app should now work on PythonAnywhere!"
