from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import AttendanceSession, AttendanceRecord
from accounts.models import User

@login_required
def attendance_list(request):
    """List all attendance sessions"""
    if request.user.team != 'PROJECT_MANAGER':
        messages.error(request, 'Only Project Managers can access attendance management.')
        return redirect('dashboard:home')
    
    sessions = AttendanceSession.objects.all().order_by('-scheduled_at')
    team_members = User.objects.filter(is_active=True).exclude(team='PROJECT_MANAGER')
    
    context = {
        'sessions': sessions,
        'team_members': team_members,
        'total_members': team_members.count()
    }
    return render(request, 'attendance/session_list.html', context)

@login_required
def create_session(request):
    """Create a new attendance session"""
    if request.user.team != 'PROJECT_MANAGER':
        messages.error(request, 'Only Project Managers can create attendance sessions.')
        return redirect('attendance:list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        scheduled_at = request.POST.get('scheduled_at')
        
        if title and scheduled_at:
            session = AttendanceSession.objects.create(
                title=title,
                description=description,
                organizer=request.user,
                scheduled_at=scheduled_at
            )
            
            messages.success(request, f'Attendance session "{session.title}" created successfully.')
            return redirect('attendance:detail', pk=session.pk)
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'attendance/create_session.html')

@login_required
def session_detail(request, pk):
    """View attendance session details"""
    if request.user.team != 'PROJECT_MANAGER':
        messages.error(request, 'Only Project Managers can access attendance details.')
        return redirect('dashboard:home')
    
    session = get_object_or_404(AttendanceSession, pk=pk)
    
    # Get attendance records for this session
    attendance_records = AttendanceRecord.objects.filter(session=session)
    attendance_data = {}
    for record in attendance_records:
        attendance_data[record.user.id] = {
            'present': record.present,
            'marked_at': record.marked_at,
            'marked_by': record.marked_by
        }
    
    context = {
        'session': session,
        'attendance_records': attendance_data,
        'attendance_stats': session.get_attendance_stats()
    }
    return render(request, 'attendance/session_detail.html', context)

@login_required
def mark_attendance(request, pk):
    """Mark attendance for team members"""
    if request.user.team != 'PROJECT_MANAGER':
        return JsonResponse({'error': 'Only Project Managers can mark attendance.'}, status=403)
    
    session = get_object_or_404(AttendanceSession, pk=pk)
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        present = request.POST.get('present') == 'true'
        
        try:
            user = User.objects.get(id=user_id)
            attendance_record, created = AttendanceRecord.objects.get_or_create(
                session=session,
                user=user,
                defaults={'present': present, 'marked_by': request.user}
            )
            
            if not created:
                attendance_record.present = present
                attendance_record.marked_by = request.user
                attendance_record.save()
            
            return JsonResponse({
                'success': True,
                'message': f'{user.name} marked as {"Present" if present else "Absent"}',
                'attendance_stats': session.get_attendance_stats()
            })
            
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
def attendance_stats(request):
    """View overall attendance statistics"""
    if request.user.team != 'PROJECT_MANAGER':
        messages.error(request, 'Only Project Managers can access attendance statistics.')
        return redirect('dashboard:home')
    
    # Get all team members
    team_members = User.objects.filter(is_active=True).exclude(team='PROJECT_MANAGER')
    
    # Calculate attendance stats for each member
    member_stats = []
    for member in team_members:
        attendance_records = AttendanceRecord.objects.filter(user=member)
        total_sessions = attendance_records.count()
        present_sessions = attendance_records.filter(present=True).count()
        attendance_rate = (present_sessions / total_sessions * 100) if total_sessions > 0 else 0
        
        member_stats.append({
            'member': member,
            'total_sessions': total_sessions,
            'present_sessions': present_sessions,
            'attendance_rate': round(attendance_rate, 1)
        })
    
    context = {
        'member_stats': member_stats,
        'total_sessions': AttendanceSession.objects.count()
    }
    return render(request, 'attendance/stats.html', context)