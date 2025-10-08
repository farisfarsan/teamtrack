from django.db import models
from django.utils import timezone
from accounts.models import User

class AttendanceSession(models.Model):
    """Represents an attendance session for team members"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_sessions")
    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.scheduled_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_attendance_count(self):
        """Get number of members marked as present"""
        return self.attendance_records.filter(present=True).count()
    
    def get_total_members(self):
        """Get total number of team members"""
        return User.objects.filter(is_active=True).exclude(team='PROJECT_MANAGER').count()
    
    def get_attendance_stats(self):
        """Get attendance statistics like 4/5"""
        present = self.get_attendance_count()
        total = self.get_total_members()
        return f"{present}/{total}"

class AttendanceRecord(models.Model):
    """Individual attendance record for a team member"""
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name="attendance_records")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    marked_at = models.DateTimeField(auto_now_add=True)
    marked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marked_attendances')
    
    class Meta:
        unique_together = ['session', 'user']
    
    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.user.name} - {self.session.title} ({status})"