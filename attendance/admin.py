from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['date', 'member', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'date']
    search_fields = ['member__username', 'member__email']
    date_hierarchy = 'date'
    ordering = ['-date', 'member__username']
