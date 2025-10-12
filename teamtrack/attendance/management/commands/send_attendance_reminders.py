from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User
from core.utils import NotificationMixin
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Send attendance reminders to all team members'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date for attendance reminder (YYYY-MM-DD). Defaults to today.',
        )

    def handle(self, *args, **options):
        # Get the date for reminders
        if options['date']:
            try:
                reminder_date = date.fromisoformat(options['date'])
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('Invalid date format. Use YYYY-MM-DD')
                )
                return
        else:
            reminder_date = timezone.now().date()

        # Get all active team members
        team_members = User.objects.filter(is_active=True)
        
        notifications_created = 0
        
        for member in team_members:
            # Create attendance reminder notification
            NotificationMixin.notify_attendance_reminder(member, reminder_date)
            notifications_created += 1
            
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully sent {notifications_created} attendance reminders for {reminder_date}'
            )
        )
