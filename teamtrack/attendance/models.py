from django.db import models
from django.utils import timezone
from accounts.models import User

class AttendanceRecord(models.Model):
    """Individual attendance record for a team member"""
    date = models.DateField(default=timezone.now)
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=10, choices=[
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ], default='Present')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['date', 'member']
        ordering = ['-date', 'member__name']
    
    def __str__(self):
        return f"{self.member.name} - {self.date} ({self.status})"
    
    @property
    def is_present(self):
        return self.status == 'Present'
    
    @property
    def is_absent(self):
        return self.status == 'Absent'
    
    @property
    def is_late(self):
        return self.status == 'Late'