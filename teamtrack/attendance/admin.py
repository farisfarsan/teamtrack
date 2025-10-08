from django.contrib import admin
from .models import AttendanceSession, AttendanceRecord

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'scheduled_at', 'created_at']
    list_filter = ['scheduled_at', 'organizer__team']
    search_fields = ['title', 'description', 'organizer__name']
    date_hierarchy = 'scheduled_at'

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'session', 'present', 'marked_at', 'marked_by']
    list_filter = ['present', 'marked_at', 'session__scheduled_at']
    search_fields = ['user__name', 'session__title']
    date_hierarchy = 'marked_at'