from django.db import models
from accounts.models import User
from django.utils import timezone
from datetime import datetime

class Meeting(models.Model):
    """Meeting model for team meetings and attendance sessions"""
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    organizer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='organized_meetings',
        help_text="User who organized this meeting"
    )
    scheduled_at = models.DateTimeField(
        default=timezone.now,
        help_text="When the meeting is scheduled"
    )
    meeting_url = models.URLField(
        blank=True, 
        null=True,
        help_text="Optional meeting URL (Zoom, Teams, etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_at']
        verbose_name = "Meeting"
        verbose_name_plural = "Meetings"
    
    def __str__(self):
        return f"{self.title} - {self.scheduled_at.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def is_upcoming(self):
        """Check if meeting is in the future"""
        return self.scheduled_at > timezone.now()
    
    @property
    def is_past(self):
        """Check if meeting is in the past"""
        return self.scheduled_at < timezone.now()


class MeetingAttendance(models.Model):
    """Attendance records for meetings"""
    
    ATTENDANCE_STATUS = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ]
    
    meeting = models.ForeignKey(
        Meeting, 
        on_delete=models.CASCADE, 
        related_name='attendance_records'
    )
    member = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='meeting_attendance'
    )
    status = models.CharField(
        max_length=20, 
        choices=ATTENDANCE_STATUS, 
        default='Present'
    )
    marked_at = models.DateTimeField(auto_now_add=True)
    marked_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='marked_attendance',
        help_text="User who marked this attendance"
    )
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['meeting', 'member']
        ordering = ['-marked_at']
        verbose_name = "Meeting Attendance"
        verbose_name_plural = "Meeting Attendance Records"
    
    def __str__(self):
        return f"{self.member.name} - {self.meeting.title} - {self.status}"
