from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.conf import settings
from .models import Task, TaskComment
from accounts.models import User
from notifications.models import Notification

@login_required
def task_list(request):
    # Get search query
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    
    # Base queryset - show tasks assigned to current user, or all tasks if Project Manager
    if request.user.team == 'PROJECT_MANAGER':
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
    
    # Pagination
    paginator = Paginator(tasks, 10)  # Show 10 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tasks': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'status_choices': Task.STATUS,
        'priority_choices': Task.PRIORITY,
    }
    
    return render(request, "tasks/task_list.html", context)

@login_required
def task_create(request):
    # Only Project Managers can create tasks
    if request.user.team != 'PROJECT_MANAGER':
        messages.error(request, 'Only Project Managers can create tasks.')
        return redirect('tasks:task_list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        assigned_to_id = request.POST.get('assigned_to')
        team = request.POST.get('team', 'TECH')
        priority = request.POST.get('priority', 'MEDIUM')
        due_date = request.POST.get('due_date')
        
        if title and assigned_to_id:
            try:
                assigned_to = User.objects.get(id=assigned_to_id)
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
                Notification.objects.create(
                    recipient=assigned_to,
                    message=f'New task assigned: "{task.title}" by {request.user.name} (Team: {task.get_team_display()})'
                )
                
                messages.success(request, f'Task "{task.title}" created and assigned to {assigned_to.name}!')
                return redirect('tasks:task_list')
            except User.DoesNotExist:
                messages.error(request, 'Invalid user selected.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
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
    # Allow viewing tasks assigned to current user, assigned by current user, or if user is Project Manager
    if (task.assigned_to != request.user and 
        task.assigned_by != request.user and 
        request.user.team != 'PROJECT_MANAGER'):
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
    
    # Only Project Managers can update tasks, or users can update their own assigned tasks
    if (request.user.team != 'PROJECT_MANAGER' and 
        task.assigned_to != request.user):
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
        if request.user.team == 'PROJECT_MANAGER':
            assigned_to_id = request.POST.get('assigned_to')
            if assigned_to_id:
                try:
                    task.assigned_to = User.objects.get(id=assigned_to_id)
                except User.DoesNotExist:
                    pass
        
        task.save()
        
        # Create notification for status changes
        if task.status == 'COMPLETED':
            Notification.objects.create(
                recipient=task.assigned_by,
                message=f'Task "{task.title}" has been completed by {task.assigned_to.name}'
            )
        
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
    
    # Only Project Managers can delete tasks
    if request.user.team != 'PROJECT_MANAGER':
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
            
            # Create notification for the manager
            if task.assigned_by:
                Notification.objects.create(
                    recipient=task.assigned_by,
                    message=f'Task "{task.title}" status changed from {old_status} to {new_status} by {request.user.name}'
                )
            
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
            
            # Create notification for the other party
            if task.assigned_to == request.user and task.assigned_by:
                # Assigned user commented, notify manager
                Notification.objects.create(
                    recipient=task.assigned_by,
                    message=f'New comment on task "{task.title}" by {request.user.name}: {message[:50]}...'
                )
            elif task.assigned_by == request.user and task.assigned_to:
                # Manager commented, notify assigned user
                Notification.objects.create(
                    recipient=task.assigned_to,
                    message=f'New comment on task "{task.title}" by {request.user.name}: {message[:50]}...'
                )
            
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Please enter a comment message.')
    
    return redirect('tasks:task_detail', pk=pk)
