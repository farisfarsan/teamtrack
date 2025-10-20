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
    
    @staticmethod
    def is_project_manager(user):
        """Check if user is a project manager"""
        return user.is_authenticated and user.is_admin
    
    @staticmethod
    def can_view_task(user, task):
        """Check if user can view a specific task"""
        if not user.is_authenticated:
            return False
        # Project managers can view all tasks
        if PermissionMixin.is_project_manager(user):
            return True
        # Users can view tasks assigned to them
        return task.assigned_to == user
    
    @staticmethod
    def can_edit_task(user, task):
        """Check if user can edit a specific task"""
        if not user.is_authenticated:
            return False
        # Project managers can edit all tasks
        if PermissionMixin.is_project_manager(user):
            return True
        # Users can edit tasks assigned to them
        return task.assigned_to == user
    
    @staticmethod
    def can_delete_task(user, task):
        """Check if user can delete a specific task"""
        if not user.is_authenticated:
            return False
        # Only project managers can delete tasks
        return PermissionMixin.is_project_manager(user)

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
    
    @staticmethod
    def paginate_queryset(queryset, request, items_per_page=20):
        """Static method to paginate a queryset"""
        paginator = Paginator(queryset, items_per_page)
        page_number = request.GET.get('page')
        return paginator.get_page(page_number)

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
    
    @staticmethod
    def notify_task_completion(task):
        """Notify about task completion"""
        try:
            from notifications.models import Notification
            Notification.objects.create(
                user=task.assigned_by,
                message=f'Task "{task.title}" has been completed by {task.assigned_to.name}',
                notification_type='success'
            )
        except ImportError:
            pass
    
    @staticmethod
    def notify_status_change(task, old_status, new_status, user):
        """Notify about status change"""
        try:
            from notifications.models import Notification
            # Notify the task creator if different from the user changing status
            if task.assigned_by != user:
                Notification.objects.create(
                    user=task.assigned_by,
                    message=f'Task "{task.title}" status changed from {old_status} to {new_status} by {user.name}',
                    notification_type='info'
                )
        except ImportError:
            pass
    
    @staticmethod
    def notify_comment(task, comment, user):
        """Notify about new comment"""
        try:
            from notifications.models import Notification
            # Notify the task creator and assignee if different from commenter
            recipients = []
            if task.assigned_by != user:
                recipients.append(task.assigned_by)
            if task.assigned_to != user and task.assigned_to != task.assigned_by:
                recipients.append(task.assigned_to)
            
            for recipient in recipients:
                Notification.objects.create(
                    user=recipient,
                    message=f'New comment on task "{task.title}" by {user.name}',
                    notification_type='info'
                )
        except ImportError:
            pass

def get_context_with_filters(request, **kwargs):
    """
    Helper function to get context with filters applied
    """
    context = {}
    
    # Add all provided kwargs to context
    context.update(kwargs)
    
    # Add search query if present
    search_query = request.GET.get('search', '')
    if search_query:
        context['search_query'] = search_query
    
    # Add filter values
    context['status_filter'] = request.GET.get('status', '')
    context['priority_filter'] = request.GET.get('priority', '')
    
    return context

def handle_task_creation(request, post_data):
    """
    Helper function to handle task creation
    """
    try:
        from tasks.models import Task
        from accounts.models import User
        
        # Create task from POST data
        task = Task.objects.create(
            title=post_data.get('title', ''),
            description=post_data.get('description', ''),
            status=post_data.get('status', 'PENDING'),
            priority=post_data.get('priority', 'MEDIUM'),
            team=post_data.get('team', 'TECH'),
            assigned_by=request.user,
            due_date=post_data.get('due_date') if post_data.get('due_date') else None
        )
        
        # Assign task to user if specified
        assigned_to_id = post_data.get('assigned_to')
        if assigned_to_id:
            try:
                task.assigned_to = User.objects.get(id=assigned_to_id)
                task.save()
            except User.DoesNotExist:
                pass
        
        return task
    except Exception as e:
        print(f"Error creating task: {e}")
        return None