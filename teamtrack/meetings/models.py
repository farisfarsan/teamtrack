from django.db import models
from accounts.models import User

class Meeting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_meetings")
    attendees = models.ManyToManyField(User, related_name="meetings", blank=True)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    location = models.CharField(max_length=200, blank=True)
    meeting_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.scheduled_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_attendance_count(self):
        """Get attendance count for this meeting"""
        return self.meetingattendance_set.filter(present=True).count()
    
    def get_total_invited(self):
        """Get total number of invited attendees"""
        return self.attendees.count()
    
    def get_attendance_stats(self):
        """Get attendance statistics like 4/5"""
        present = self.get_attendance_count()
        total = self.get_total_invited()
        return f"{present}/{total}"

class MeetingAttendance(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    marked_at = models.DateTimeField(auto_now_add=True)
    marked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marked_attendances')
    
    class Meta:
        unique_together = ['meeting', 'user']
    
    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.user.name} - {self.meeting.title} ({status})"