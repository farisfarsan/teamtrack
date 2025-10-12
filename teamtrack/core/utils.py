"""
Shared utility functions and mixins to reduce code duplication.
"""

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.db import transaction
from .constants import ITEMS_PER_PAGE


class PermissionMixin:
    """Mixin to handle common permission checks."""
    
    @staticmethod
    def is_project_manager(user):
        """Check if user is a project manager."""
        return user.team == 'PROJECT_MANAGER'
    
    @staticmethod
    def can_view_task(user, task):
        """Check if user can view a specific task."""
        return (task.assigned_to == user or 
                task.assigned_by == user or 
                PermissionMixin.is_project_manager(user))
    
    @staticmethod
    def can_edit_task(user, task):
        """Check if user can edit a specific task."""
        return (PermissionMixin.is_project_manager(user) or 
                task.assigned_to == user)
    
    @staticmethod
    def can_delete_task(user, task):
        """Check if user can delete a specific task."""
        return PermissionMixin.is_project_manager(user)


class TaskFilterMixin:
    """Mixin to handle common task filtering logic."""
    
    @staticmethod
    def get_filtered_tasks(user, search_query='', status_filter='', priority_filter=''):
        """Get filtered tasks based on user permissions and filters."""
        # Base queryset - show tasks assigned to current user, or all tasks if Project Manager
        if PermissionMixin.is_project_manager(user):
            tasks = user.assigned_tasks.all()  # This will be replaced with actual Task model
        else:
            tasks = user.tasks.all()
        
        # Apply filters
        if search_query:
            tasks = tasks.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        if status_filter:
            tasks = tasks.filter(status=status_filter)
        
        if priority_filter:
            tasks = tasks.filter(priority=priority_filter)
        
        # Order by creation date (newest first)
        return tasks.order_by('-created_at')


class PaginationMixin:
    """Mixin to handle pagination logic."""
    
    @staticmethod
    def paginate_queryset(queryset, request, items_per_page=ITEMS_PER_PAGE):
        """Paginate a queryset."""
        paginator = Paginator(queryset, items_per_page)
        page_number = request.GET.get('page')
        return paginator.get_page(page_number)


class NotificationMixin:
    """Mixin to handle notification creation."""
    
    @staticmethod
    def create_notification(recipient, message):
        """Create a notification for a user."""
        from teamtrack.notifications.models import Notification
        return Notification.objects.create(
            recipient=recipient,
            message=message
        )
    
    @staticmethod
    def notify_task_assignment(assigned_to, task, assigned_by):
        """Create notification for task assignment."""
        message = f'New task assigned: "{task.title}" by {assigned_by.name} (Team: {task.get_team_display()})'
        return NotificationMixin.create_notification(assigned_to, message)
    
    @staticmethod
    def notify_task_completion(task):
        """Create notification for task completion."""
        if task.assigned_by:
            message = f'Task "{task.title}" has been completed by {task.assigned_to.name}'
            return NotificationMixin.create_notification(task.assigned_by, message)
    
    @staticmethod
    def notify_status_change(task, old_status, new_status, changed_by):
        """Create notification for task status change."""
        if task.assigned_by:
            message = f'Task "{task.title}" status changed from {old_status} to {new_status} by {changed_by.name}'
            return NotificationMixin.create_notification(task.assigned_by, message)
    
    @staticmethod
    def notify_comment(task, comment, author):
        """Create notification for task comment."""
        if task.assigned_to == author and task.assigned_by:
            # Assigned user commented, notify manager
            recipient = task.assigned_by
        elif task.assigned_by == author and task.assigned_to:
            # Manager commented, notify assigned user
            recipient = task.assigned_to
        else:
            return None
        
        message = f'New comment on task "{task.title}" by {author.name}: {comment.message[:50]}...'
        return NotificationMixin.create_notification(recipient, message)
    
    @staticmethod
    def notify_attendance_marked(member, date, status, marked_by):
        """Create notification for attendance marking."""
        message = f'Your attendance for {date} has been marked as {status} by {marked_by.name}'
        return NotificationMixin.create_notification(member, message)
    
    @staticmethod
    def notify_attendance_reminder(member, date):
        """Create notification for attendance reminder."""
        message = f'Reminder: Please mark your attendance for {date}'
        return NotificationMixin.create_notification(member, message)
    
    @staticmethod
    def notify_attendance_summary(manager, date, present_count, total_count):
        """Create notification for attendance summary to manager."""
        message = f'Attendance summary for {date}: {present_count}/{total_count} members present'
        return NotificationMixin.create_notification(manager, message)
    
    @staticmethod
    def notify_attendance_session_created(manager, session_name, date):
        """Create notification for new attendance session."""
        message = f'New attendance session "{session_name}" created for {date}'
        return NotificationMixin.create_notification(manager, message)


def get_context_with_filters(request, **extra_context):
    """Get common context with filter parameters."""
    context = {
        'search_query': request.GET.get('search', ''),
        'status_filter': request.GET.get('status', ''),
        'priority_filter': request.GET.get('priority', ''),
    }
    context.update(extra_context)
    return context


def handle_task_creation(request, task_data):
    """Handle task creation with proper error handling and notifications."""
    from teamtrack.accounts.models import User
    from teamtrack.tasks.models import Task
    from .constants import TASK_PRIORITY, TEAMS
    
    title = task_data.get('title', '').strip()
    description = task_data.get('description', '').strip()
    assigned_to_id = task_data.get('assigned_to')
    team = task_data.get('team', 'TECH')
    priority = task_data.get('priority', 'MEDIUM')
    due_date = task_data.get('due_date')
    
    # Validate required fields
    if not title:
        messages.error(request, 'Task title is required.')
        return None
    elif not assigned_to_id:
        messages.error(request, 'Please select a user to assign the task to.')
        return None
    
    try:
        # Use database transaction to ensure data consistency
        with transaction.atomic():
            assigned_to = User.objects.get(id=assigned_to_id, is_active=True)
            
            # Create the task
            task = Task.objects.create(
                title=title,
                description=description,
                assigned_to=assigned_to,
                assigned_by=request.user,
                team=team,
                priority=priority,
                due_date=due_date if due_date else None
            )
            
            # Create notification for the assigned user
            NotificationMixin.notify_task_assignment(assigned_to, task, request.user)
            
            # Verify task was created successfully
            if Task.objects.filter(id=task.id).exists():
                messages.success(request, f'Task "{task.title}" created and assigned to {assigned_to.name}!')
                return task
            else:
                messages.error(request, 'Task creation failed. Please try again.')
                return None
                
    except User.DoesNotExist:
        messages.error(request, 'Selected user not found or inactive.')
        return None
    except Exception as e:
        messages.error(request, f'Error creating task: {str(e)}')
        return None
