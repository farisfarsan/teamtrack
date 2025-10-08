from django.core.management.base import BaseCommand
from django.core.cache import cache
from tasks.models import Task, TaskComment
from meetings.models import Meeting
from notifications.models import Notification
from accounts.models import User

class Command(BaseCommand):
    help = 'Reset production database to clean state'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all data',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  This will delete ALL tasks, meetings, and notifications!'
                )
            )
            self.stdout.write('Run with --confirm to proceed')
            return

        self.stdout.write('🧹 Resetting production database...')
        
        # Clear cache
        cache.clear()
        self.stdout.write('✅ Cache cleared')
        
        # Delete all tasks and related data
        task_count = Task.objects.count()
        comment_count = TaskComment.objects.count()
        meeting_count = Meeting.objects.count()
        notification_count = Notification.objects.count()
        
        self.stdout.write(f'📊 Current data:')
        self.stdout.write(f'  - Tasks: {task_count}')
        self.stdout.write(f'  - Comments: {comment_count}')
        self.stdout.write(f'  - Meetings: {meeting_count}')
        self.stdout.write(f'  - Notifications: {notification_count}')
        
        # Delete all data
        TaskComment.objects.all().delete()
        Task.objects.all().delete()
        Meeting.objects.all().delete()
        Notification.objects.all().delete()
        
        self.stdout.write('✅ All data cleared')
        
        # Verify cleanup
        remaining_tasks = Task.objects.count()
        remaining_comments = TaskComment.objects.count()
        remaining_meetings = Meeting.objects.count()
        remaining_notifications = Notification.objects.count()
        
        self.stdout.write(f'📊 After cleanup:')
        self.stdout.write(f'  - Tasks: {remaining_tasks}')
        self.stdout.write(f'  - Comments: {remaining_comments}')
        self.stdout.write(f'  - Meetings: {remaining_meetings}')
        self.stdout.write(f'  - Notifications: {remaining_notifications}')
        
        # Show remaining users
        user_count = User.objects.count()
        self.stdout.write(f'👥 Users preserved: {user_count}')
        
        self.stdout.write('\n✅ Database reset completed!')
        self.stdout.write('🎯 Dashboard should now show accurate data')
