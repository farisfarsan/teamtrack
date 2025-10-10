from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.conf import settings
from django.db import transaction
from .models import Task, TaskComment
from accounts.models import User
from notifications.models import Notification
from core.utils import (
    PermissionMixin, TaskFilterMixin, PaginationMixin, NotificationMixin,
    get_context_with_filters, handle_task_creation
)
from core.constants import ITEMS_PER_PAGE

@login_required
def task_list(request):
    # Get filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    
    # Get filtered tasks using shared utility
    if PermissionMixin.is_project_manager(request.user):
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)
    
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
    tasks = tasks.order_by('-created_at')
    
    # Pagination using shared utility
    page_obj = PaginationMixin.paginate_queryset(tasks, request, ITEMS_PER_PAGE)
    
    # Get context with filters using shared utility
    context = get_context_with_filters(request, 
        page_obj=page_obj,
        tasks=page_obj,
        status_choices=Task.STATUS,
        priority_choices=Task.PRIORITY,
    )
    
    return render(request, "tasks/task_list.html", context)

@login_required
def task_create(request):
    # Only Project Managers can create tasks
    if not PermissionMixin.is_project_manager(request.user):
        messages.error(request, 'Only Project Managers can create tasks.')
        return redirect('tasks:task_list')
    
    if request.method == 'POST':
        task = handle_task_creation(request, request.POST)
        if task:
            return redirect('tasks:task_detail', pk=task.pk)
    
    # Get all users for assignment dropdown
    users = User.objects.filter(is_active=True)
    context = {
        'users': users,
        'priority_choices': Task.PRIORITY,
        'team_choices': Task.TEAMS,
    }
    return render(request, 'tasks/task_create.html', context)

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    # Check permissions using shared utility
    if not PermissionMixin.can_view_task(request.user, task):
        messages.error(request, 'You do not have permission to view this task.')
        return redirect('tasks:task_list')
    
    # Get comments for this task
    comments = task.comments.all()
    
    context = {
        'task': task,
        'comments': comments,
        'comment_types': TaskComment.COMMENT_TYPES,
    }
    return render(request, 'tasks/task_detail.html', context)

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    # Check permissions using shared utility
    if not PermissionMixin.can_edit_task(request.user, task):
        messages.error(request, 'You can only edit tasks assigned to you or you must be a Project Manager.')
        return redirect('tasks:task_list')
    
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.status = request.POST.get('status', task.status)
        task.priority = request.POST.get('priority', task.priority)
        task.team = request.POST.get('team', task.team)
        task.due_date = request.POST.get('due_date') if request.POST.get('due_date') else None
        
        # Only allow changing assignee if user is Project Manager
        if PermissionMixin.is_project_manager(request.user):
            assigned_to_id = request.POST.get('assigned_to')
            if assigned_to_id:
                try:
                    task.assigned_to = User.objects.get(id=assigned_to_id)
                except User.DoesNotExist:
                    pass
        
        task.save()
        
        # Create notification for status changes using shared utility
        if task.status == 'COMPLETED':
            NotificationMixin.notify_task_completion(task)
        
        messages.success(request, f'Task "{task.title}" updated successfully!')
        return redirect('tasks:task_detail', pk=task.pk)
    
    users = User.objects.filter(is_active=True)
    context = {
        'task': task,
        'users': users,
        'status_choices': Task.STATUS,
        'priority_choices': Task.PRIORITY,
    }
    return render(request, 'tasks/task_update.html', context)

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    # Check permissions using shared utility
    if not PermissionMixin.can_delete_task(request.user, task):
        messages.error(request, 'Only Project Managers can delete tasks.')
        return redirect('tasks:task_list')
    
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'Task "{task_title}" deleted successfully!')
        return redirect('tasks:task_list')
    
    return render(request, 'tasks/task_delete.html', {'task': task})

@login_required
def task_status_update(request, pk):
    """Allow team members to update their task status"""
    task = get_object_or_404(Task, pk=pk)
    
    # Only allow the assigned user to update status
    if task.assigned_to != request.user:
        messages.error(request, 'You can only update tasks assigned to you.')
        return redirect('tasks:task_detail', pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [choice[0] for choice in Task.STATUS]:
            old_status = task.status
            task.status = new_status
            task.save()
            
            # Create notification using shared utility
            NotificationMixin.notify_status_change(task, old_status, new_status, request.user)
            
            messages.success(request, f'Task status updated to {task.get_status_display()}')
        else:
            messages.error(request, 'Invalid status selected.')
    
    return redirect('tasks:task_detail', pk=pk)

@login_required
def task_add_comment(request, pk):
    """Allow team members to add comments to their tasks"""
    task = get_object_or_404(Task, pk=pk)
    
    # Only allow the assigned user or manager to add comments
    if task.assigned_to != request.user and task.assigned_by != request.user:
        messages.error(request, 'You can only comment on tasks assigned to you or created by you.')
        return redirect('tasks:task_detail', pk=pk)
    
    if request.method == 'POST':
        comment_type = request.POST.get('comment_type', 'GENERAL')
        message = request.POST.get('message', '').strip()
        attachment = request.FILES.get('attachment')
        
        if message:
            comment = TaskComment.objects.create(
                task=task,
                author=request.user,
                comment_type=comment_type,
                message=message,
                attachment=attachment
            )
            
            # Create notification using shared utility
            NotificationMixin.notify_comment(task, comment, request.user)
            
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Please enter a comment message.')
    
    return redirect('tasks:task_detail', pk=pk)
