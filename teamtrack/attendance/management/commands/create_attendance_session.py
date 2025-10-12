from django.core.management.base import BaseCommand
from django.utils import timezone
from teamtrack.accounts.models import User
from teamtrack.core.utils import NotificationMixin
from datetime import date


class Command(BaseCommand):
    help = 'Create a new attendance session and notify managers'

    def add_arguments(self, parser):
        parser.add_argument(
            'session_name',
            type=str,
            help='Name of the attendance session',
        )
        parser.add_argument(
            '--date',
            type=str,
            help='Date for the session (YYYY-MM-DD). Defaults to today.',
        )

    def handle(self, *args, **options):
        session_name = options['session_name']
        
        # Get the date for the session
        if options['date']:
            try:
                session_date = date.fromisoformat(options['date'])
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('Invalid date format. Use YYYY-MM-DD')
                )
                return
        else:
            session_date = timezone.now().date()

        # Get all project managers
        managers = User.objects.filter(
            is_active=True, 
            team='PROJECT_MANAGER'
        )
        
        notifications_created = 0
        
        for manager in managers:
            # Create attendance session notification
            NotificationMixin.notify_attendance_session_created(
                manager, session_name, session_date
            )
            notifications_created += 1
            
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created attendance session "{session_name}" '
                f'for {session_date} and notified {notifications_created} managers'
            )
        )
