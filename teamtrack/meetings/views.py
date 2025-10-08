from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Meeting, MeetingAttendance
from accounts.models import User

@login_required
def meeting_list(request):
    # Only Project Managers can access meetings page
    if request.user.team != 'PROJECT_MANAGER':
        messages.error(request, 'Only Project Managers can access meetings.')
        return redirect('dashboard:home')
    
    meetings = Meeting.objects.all().order_by('-scheduled_at')
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
    
    # Get attendance records for this meeting
    attendance_records = MeetingAttendance.objects.filter(meeting=meeting)
    attendance_data = {}
    for record in attendance_records:
        attendance_data[record.user.id] = {
            'present': record.present,
            'marked_at': record.marked_at,
            'marked_by': record.marked_by
        }
    
    context = {
        'meeting': meeting,
        'attendance_records': attendance_data,
        'attendance_stats': meeting.get_attendance_stats()
    }
    return render(request, 'meetings/detail.html', context)

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

@login_required
def attendance_management(request, pk):
    """Admin dashboard for marking attendance by meeting date"""
    if request.user.team != 'PROJECT_MANAGER':
        messages.error(request, 'Only Project Managers can manage attendance.')
        return redirect('dashboard:home')
    
    meeting = get_object_or_404(Meeting, pk=pk)
    
    if request.method == 'POST':
        # Process attendance marking
        for attendee in meeting.attendees.all():
            present_key = f'attendance_{attendee.id}'
            is_present = present_key in request.POST
            
            # Get or create attendance record
            attendance, created = MeetingAttendance.objects.get_or_create(
                meeting=meeting,
                user=attendee,
                defaults={'present': is_present, 'marked_by': request.user}
            )
            
            if not created:
                attendance.present = is_present
                attendance.marked_by = request.user
                attendance.save()
        
        messages.success(request, f'Attendance marked for {meeting.title}')
        return redirect('meetings:detail', pk=pk)
    
    # Get attendance records for this meeting
    attendance_records = {}
    for attendee in meeting.attendees.all():
        try:
            record = MeetingAttendance.objects.get(meeting=meeting, user=attendee)
            attendance_records[attendee.id] = record.present
        except MeetingAttendance.DoesNotExist:
            attendance_records[attendee.id] = False
    
    context = {
        'meeting': meeting,
        'attendance_records': attendance_records,
        'attendance_stats': meeting.get_attendance_stats()
    }
    return render(request, 'meetings/attendance_management.html', context)

@login_required
def attendance_stats(request):
    """Show attendance statistics for all meetings"""
    if request.user.team != 'PROJECT_MANAGER':
        messages.error(request, 'Only Project Managers can view attendance statistics.')
        return redirect('dashboard:home')
    
    meetings = Meeting.objects.all().order_by('-scheduled_at')
    meeting_stats = []
    
    for meeting in meetings:
        stats = {
            'meeting': meeting,
            'attendance_count': meeting.get_attendance_count(),
            'total_invited': meeting.get_total_invited(),
            'attendance_rate': (meeting.get_attendance_count() / meeting.get_total_invited() * 100) if meeting.get_total_invited() > 0 else 0,
            'absent_count': meeting.get_total_invited() - meeting.get_attendance_count()
        }
        meeting_stats.append(stats)
    
    context = {
        'meeting_stats': meeting_stats
    }
    return render(request, 'meetings/attendance_stats.html', context)
