from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'List all users with their credentials'

    def handle(self, *args, **options):
        users = User.objects.all().order_by('team', 'name')
        
        self.stdout.write('=== ALL USER CREDENTIALS ===')
        self.stdout.write('')
        
        for user in users:
            self.stdout.write(f'Name: {user.name}')
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'Team: {user.get_team_display()}')
            self.stdout.write('---')
