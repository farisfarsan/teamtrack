"""
Management command to set up attendance tables and initial data
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from attendance.models import AttendanceRecord


class Command(BaseCommand):
    help = 'Set up attendance tables and initial data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up attendance tables...')
        
        try:
            # Run migrations
            call_command('makemigrations', 'attendance', verbosity=0)
            call_command('migrate', 'attendance', verbosity=0)
            
            # Check if table exists
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLES LIKE 'attendance_attendancerecord'")
                table_exists = cursor.fetchone()
                
                if table_exists:
                    self.stdout.write(
                        self.style.SUCCESS('✓ Attendance table created successfully')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR('✗ Attendance table was not created')
                    )
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error setting up attendance: {e}')
            )
