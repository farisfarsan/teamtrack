from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import AttendanceRecord

User = get_user_model()

@login_required
def attendance_list(request):
    """List all attendance records"""
    # Simplified: allow all authenticated users to view attendance
    # Get attendance records grouped by date
    records = AttendanceRecord.objects.all().order_by('-date', 'member__username')
    
    # Group records by date
    attendance_by_date = {}
    for record in records:
        date_key = record.date.strftime('%Y-%m-%d')
        if date_key not in attendance_by_date:
            attendance_by_date[date_key] = []
        attendance_by_date[date_key].append(record)
    
    # Get all users for creating new records
    team_members = User.objects.filter(is_active=True)
    
    context = {
        'attendance_by_date': attendance_by_date,
        'team_members': team_members,
        'total_members': team_members.count(),
        'total_records': records.count(),
        'active_members': team_members.filter(attendance_records__status='Present').distinct().count()
    }
    return render(request, 'attendance/session_list.html', context)

@login_required
def mark_attendance(request):
    """Modal-based attendance marking"""
    # Simplified: allow all authenticated users to mark attendance
    
    if request.method == 'POST':
        date = request.POST.get('date')
        present_user_ids = request.POST.getlist('present_users[]')
        
        if not date:
            return JsonResponse({'error': 'Date is required.'}, status=400)
        
        # Get all users
        team_members = User.objects.filter(is_active=True)
        
        # Create/update attendance records
        for member in team_members:
            status = 'Present' if str(member.id) in present_user_ids else 'Absent'
            AttendanceRecord.objects.update_or_create(
                member=member,
                date=date,
                defaults={'status': status}
            )
        
        return JsonResponse({
            'success': True,
            'message': f'Attendance marked for {date}',
            'present_count': len(present_user_ids),
            'total_count': team_members.count()
        })
    
    # GET request - show the marking interface
    team_members = User.objects.filter(is_active=True).order_by('username')
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