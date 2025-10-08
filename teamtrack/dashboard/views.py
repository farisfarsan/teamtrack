from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from tasks.models import Task
from notifications.models import Notification

@login_required
def home_redirect(request):
    if request.user.team == "PROJECT_MANAGER":
        return redirect("dashboard:admin")
    else:
        return redirect("dashboard:member")

@login_required
def admin_dashboard(request):
    # Task analytics - ALL tasks in the system
    all_tasks = Task.objects.all()
    total_tasks = all_tasks.count()
    completed_tasks = all_tasks.filter(status="COMPLETED").count()
    pending_tasks = all_tasks.filter(status="PENDING").count()
    in_progress_tasks = all_tasks.filter(status="IN_PROGRESS").count()
    overdue_tasks = all_tasks.filter(
        status__in=["PENDING", "IN_PROGRESS"], 
        due_date__lt=timezone.now().date()
    ).count()
    
    # Team-based task distribution
    team_stats = {}
    for team_code, team_name in User.TEAMS:
        team_users = User.objects.filter(team=team_code)
        team_tasks = Task.objects.filter(assigned_to__in=team_users)
        team_pending = team_tasks.filter(status="PENDING").count()
        team_stats[team_name] = {
            'total': team_tasks.count(),
            'pending': team_pending,
            'completed': team_tasks.filter(status="COMPLETED").count(),
            'in_progress': team_tasks.filter(status="IN_PROGRESS").count(),
            'users': team_users.count()
        }
    
    # User analytics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    team_members = User.objects.filter(is_active=True).exclude(team='PROJECT_MANAGER')
    
    # Recent activity - ALL tasks
    recent_tasks = all_tasks.order_by('-created_at')[:10]
    
    # All tasks for admin view
    all_tasks_list = all_tasks.order_by('-created_at')
    
    data = {
        "all_tasks": all_tasks_list,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "overdue_tasks": overdue_tasks,
        "total_users": total_users,
        "active_users": active_users,
        "team_members": team_members,
        "recent_tasks": recent_tasks,
        "completion_rate": round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1),
        "team_stats": team_stats,
    }
    return render(request,"dashboard/admin.html", data)

@login_required
def manager_dashboard(request):
    # Tasks assigned by this manager
    assigned_tasks = Task.objects.filter(assigned_by=request.user)
    total_assigned = assigned_tasks.count()
    completed_assigned = assigned_tasks.filter(status="COMPLETED").count()
    pending_assigned = assigned_tasks.filter(status="PENDING").count()
    
    # Team members
    team_members = User.objects.filter(
        tasks__assigned_by=request.user
    ).distinct()
    
    # Recent tasks
    recent_tasks = assigned_tasks.order_by('-created_at')[:5]
    
    data = {
        "assigned_tasks": assigned_tasks,
        "total_assigned": total_assigned,
        "completed_assigned": completed_assigned,
        "pending_assigned": pending_assigned,
        "team_members": team_members,
        "recent_tasks": recent_tasks,
        "completion_rate": round((completed_assigned / total_assigned * 100) if total_assigned > 0 else 0, 1),
    }
    return render(request,"dashboard/manager.html", data)

@login_required
def member_dashboard(request):
    # User's tasks
    user_tasks = Task.objects.filter(assigned_to=request.user)
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(status="COMPLETED").count()
    pending_tasks = user_tasks.filter(status="PENDING").count()
    in_progress_tasks = user_tasks.filter(status="IN_PROGRESS").count()
    overdue_tasks = user_tasks.filter(
        status__in=["PENDING", "IN_PROGRESS"], 
        due_date__lt=timezone.now().date()
    ).count()
    
    # All tasks from all teams (for dashboard visibility)
    all_team_tasks = Task.objects.all().order_by('-created_at')
    
    # Team tasks (all pending tasks for the user's team)
    team_users = User.objects.filter(team=request.user.team)
    team_tasks = Task.objects.filter(
        assigned_to__in=team_users,
        status="PENDING"
    ).order_by('-created_at')
    
    # Recent notifications
    recent_notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')[:5]
    
    # Recent tasks
    recent_tasks = user_tasks.order_by('-created_at')[:5]
    
    data = {
        "tasks": user_tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "overdue_tasks": overdue_tasks,
        "recent_notifications": recent_notifications,
        "recent_tasks": recent_tasks,
        "completion_rate": round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1),
        "team_tasks": team_tasks,
        "all_team_tasks": all_team_tasks,
        "team_name": request.user.get_team_display(),
    }
    return render(request,"dashboard/member.html", data)
