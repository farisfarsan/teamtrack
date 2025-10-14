from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a new user'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='User email')
        parser.add_argument('--password', type=str, help='User password')
        parser.add_argument('--name', type=str, help='User name')

    def handle(self, *args, **options):
        email = options.get('email') or 'kiranmoorkath@gmail.com'
        password = options.get('password') or 'kiran123'
        name = options.get('name') or 'Kiran Moorkath'
        
        try:
            if User.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(f'User {email} already exists!')
                )
                user = User.objects.get(email=email)
                self.stdout.write(f'Existing user: {user.name} ({user.email})')
            else:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    name=name,
                    is_active=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f'User created successfully!')
                )
                self.stdout.write(f'Name: {user.name}')
                self.stdout.write(f'Email: {user.email}')
                self.stdout.write(f'Team: {user.get_team_display()}')
                self.stdout.write(f'Active: {user.is_active}')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating user: {e}')
            )
