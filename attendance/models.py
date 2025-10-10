from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]
    
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Absent')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['member', 'date']
        ordering = ['-date', 'member__username']
    
    def __str__(self):
        return f"{self.member.username} - {self.date} - {self.status}"
    
    @property
    def is_present(self):
        return self.status == 'Present'
    
    @property
    def is_absent(self):
        return self.status == 'Absent'
    
    @property
    def is_late(self):
        return self.status == 'Late'
