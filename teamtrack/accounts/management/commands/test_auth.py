from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from accounts.models import User


class Command(BaseCommand):
    help = 'Test authentication functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='admin@example.com',
            help='Email to test authentication with',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Password to test authentication with',
        )

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        
        self.stdout.write(f'Testing authentication for: {email}')
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
            self.stdout.write(f'User found: {user.name} ({user.email})')
            self.stdout.write(f'User is_active: {user.is_active}')
            self.stdout.write(f'User is_staff: {user.is_staff}')
            self.stdout.write(f'User is_superuser: {user.is_superuser}')
            
            # Test password check
            if user.check_password(password):
                self.stdout.write(self.style.SUCCESS('Password check: PASSED'))
            else:
                self.stdout.write(self.style.ERROR('Password check: FAILED'))
                
            # Test authentication
            auth_user = authenticate(email=email, password=password)
            if auth_user:
                self.stdout.write(self.style.SUCCESS(f'Authentication: PASSED - {auth_user.name}'))
            else:
                self.stdout.write(self.style.ERROR('Authentication: FAILED'))
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User not found: {email}'))
            
        # List all users
        self.stdout.write('\nAll users in database:')
        for user in User.objects.all():
            self.stdout.write(f'- {user.email} ({user.name}) - Active: {user.is_active}')
