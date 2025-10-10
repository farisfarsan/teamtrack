from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['date', 'member', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'date', 'member__team']
    search_fields = ['member__name', 'member__email']
    date_hierarchy = 'date'
    ordering = ['-date', 'member__name']
