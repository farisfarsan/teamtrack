from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Meeting

@login_required
def meeting_list(request):
    # Only Project Managers can access meetings page
    if request.user.team != 'PROJECT_MANAGER':
        messages.error(request, 'Only Project Managers can access meetings.')
        return redirect('dashboard:home')
    
    meetings = Meeting.objects.filter(attendees=request.user).order_by('-scheduled_at')
    return render(request, 'meetings/meeting_list.html', {'meetings': meetings})

@login_required
def create_meeting(request):
    # Only Project Managers can create meetings
    if request.user.team != 'PROJECT_MANAGER':
        messages.error(request, 'Only Project Managers can create meetings.')
        return redirect('meetings:list')
    
    if request.method == 'POST':
        # Basic meeting creation logic
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        scheduled_at = request.POST.get('scheduled_at')
        
        if title and scheduled_at:
            meeting = Meeting.objects.create(
                title=title,
                description=description,
                organizer=request.user,
                scheduled_at=scheduled_at
            )
            meeting.attendees.add(request.user)
            
            # Send notifications to all team members
            from notifications.models import Notification
            from accounts.models import User
            
            # Get all team members (excluding the organizer)
            team_members = User.objects.filter(is_active=True).exclude(id=request.user.id)
            
            for member in team_members:
                Notification.objects.create(
                    recipient=member,
                    message=f'New meeting scheduled: "{meeting.title}" by {request.user.name} on {meeting.scheduled_at.strftime("%B %d, %Y at %H:%M")}'
                )
            
            messages.success(request, f'Meeting created successfully! Notifications sent to {team_members.count()} team members.')
            return redirect('meetings:detail', pk=meeting.pk)
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'meetings/create.html')

@login_required
def meeting_detail(request, pk):
    # Only Project Managers can access meeting details
    if request.user.team != 'PROJECT_MANAGER':
        messages.error(request, 'Only Project Managers can access meeting details.')
        return redirect('dashboard:home')
    
    meeting = get_object_or_404(Meeting, pk=pk)
    return render(request, 'meetings/detail.html', {'meeting': meeting})

@login_required
def mark_attendance(request, pk):
    # Only Project Managers can mark attendance
    if request.user.team != 'PROJECT_MANAGER':
        return JsonResponse({
            'success': False,
            'message': 'Only Project Managers can mark attendance.'
        })
    
    if request.method == 'POST':
        meeting = get_object_or_404(Meeting, pk=pk)
        
        # Add current user to attendees if not already present
        if request.user not in meeting.attendees.all():
            meeting.attendees.add(request.user)
            
        return JsonResponse({
            'success': True,
            'attendance_count': meeting.attendees.count(),
            'message': 'Attendance marked successfully!'
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })
