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
    """List attendance records - all records for managers/admins, own records for members"""
    
    # Check if user is manager or admin
    is_manager_or_admin = request.user.team == 'PROJECT_MANAGER' or request.user.is_superuser
    
    if is_manager_or_admin:
        # Managers/admins can see all attendance records
        records = AttendanceRecord.objects.all().order_by('-date', 'member__name')
        team_members = User.objects.filter(is_active=True)
        total_members = team_members.count()
        active_members = team_members.filter(attendance_records__status='Present').distinct().count()
    else:
        # Regular members can only see their own attendance records
        records = AttendanceRecord.objects.filter(member=request.user).order_by('-date')
        team_members = User.objects.filter(id=request.user.id)
        total_members = 1
        active_members = 1 if records.filter(status='Present').exists() else 0
    
    # Group records by date
    attendance_by_date = {}
    for record in records:
        date_key = record.date.strftime('%Y-%m-%d')
        if date_key not in attendance_by_date:
            attendance_by_date[date_key] = []
        attendance_by_date[date_key].append(record)
    
    context = {
        'attendance_by_date': attendance_by_date,
        'team_members': team_members,
        'total_members': total_members,
        'total_records': records.count(),
        'active_members': active_members,
        'is_manager_or_admin': is_manager_or_admin,
    }
    return render(request, 'attendance/session_list.html', context)

@login_required
def mark_attendance(request):
    """Modal-based attendance marking"""
    if request.user.team != 'PROJECT_MANAGER' and not request.user.is_superuser:
        return JsonResponse({'error': 'Only Project Managers and Admins can mark attendance.'}, status=403)
    
    if request.method == 'POST':
        date = request.POST.get('date')
        present_user_ids = request.POST.getlist('present_users[]')
        
        if not date:
            return JsonResponse({'error': 'Date is required.'}, status=400)
        
        # Get all team members
        team_members = User.objects.filter(is_active=True)
        
        # Create/update attendance records
        for member in team_members:
            status = 'Present' if str(member.id) in present_user_ids else 'Absent'
            AttendanceRecord.objects.update_or_create(
                member=member,
                date=date,
                defaults={'status': status}
            )
            
            # Create notification for each member
            from core.utils import NotificationMixin
            NotificationMixin.notify_attendance_marked(member, date, status, request.user)
        
        # Create summary notification for manager
        from core.utils import NotificationMixin
        NotificationMixin.notify_attendance_summary(
            request.user, date, len(present_user_ids), team_members.count()
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Attendance marked for {date}',
            'present_count': len(present_user_ids),
            'total_count': team_members.count()
        })
    
    # GET request - show the marking interface
    team_members = User.objects.filter(is_active=True).order_by('name')
    today = timezone.now().date()
    
    # Get existing attendance for today
    existing_records = AttendanceRecord.objects.filter(date=today)
    present_user_ids = [str(record.member.id) for record in existing_records.filter(status='Present')]
    
    context = {
        'team_members': team_members,
        'today': today,
        'present_user_ids': present_user_ids
    }
    return render(request, 'attendance/mark_attendance.html', context)