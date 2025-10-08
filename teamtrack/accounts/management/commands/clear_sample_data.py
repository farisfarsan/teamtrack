from django.core.management.base import BaseCommand
from django.db import transaction
from tasks.models import Task
from meetings.models import Meeting
from notifications.models import Notification
from accounts.models import User

class Command(BaseCommand):
    help = 'Remove all sample data from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all sample data',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING('⚠️  This will delete ALL sample data!')
            )
            self.stdout.write('Sample data includes:')
            self.stdout.write('- All Tasks')
            self.stdout.write('- All Meetings') 
            self.stdout.write('- All Notifications')
            self.stdout.write('')
            self.stdout.write('User accounts will be preserved.')
            self.stdout.write('')
            self.stdout.write('To proceed, run: python manage.py clear_sample_data --confirm')
            return

        with transaction.atomic():
            # Count existing data
            task_count = Task.objects.count()
            meeting_count = Meeting.objects.count()
            notification_count = Notification.objects.count()
            
            self.stdout.write(f'📊 Current data:')
            self.stdout.write(f'   Tasks: {task_count}')
            self.stdout.write(f'   Meetings: {meeting_count}')
            self.stdout.write(f'   Notifications: {notification_count}')
            self.stdout.write('')

            # Delete all sample data
            deleted_tasks = Task.objects.all().delete()
            deleted_meetings = Meeting.objects.all().delete()
            deleted_notifications = Notification.objects.all().delete()

            self.stdout.write(self.style.SUCCESS('🗑️  Sample data cleared successfully!'))
            self.stdout.write('')
            self.stdout.write(f'✅ Deleted {deleted_tasks[0]} tasks')
            self.stdout.write(f'✅ Deleted {deleted_meetings[0]} meetings')
            self.stdout.write(f'✅ Deleted {deleted_notifications[0]} notifications')
            self.stdout.write('')
            
            # Show remaining users
            user_count = User.objects.count()
            self.stdout.write(f'👥 User accounts preserved: {user_count} users')
            self.stdout.write('')
            self.stdout.write('📋 Remaining users:')
            for user in User.objects.all().order_by('team', 'name'):
                self.stdout.write(f'   {user.name} ({user.email}) - {user.get_team_display()}')
            
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('🎉 Database is now clean and ready for production use!'))
