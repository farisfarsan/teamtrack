from django.contrib import admin
from .models import Meeting, MeetingAttendance

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'scheduled_at', 'duration_minutes', 'location']
    list_filter = ['scheduled_at', 'organizer__team']
    search_fields = ['title', 'description', 'organizer__name']
    date_hierarchy = 'scheduled_at'
    filter_horizontal = ['attendees']

@admin.register(MeetingAttendance)
class MeetingAttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'meeting', 'present', 'marked_at', 'marked_by']
    list_filter = ['present', 'marked_at', 'meeting__scheduled_at']
    search_fields = ['user__name', 'meeting__title']
    date_hierarchy = 'marked_at'
