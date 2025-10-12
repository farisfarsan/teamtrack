from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Create initial users for Render deployment'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create admin user
            admin_email = 'admin@example.com'
            admin_password = 'admin123'
            
            if not User.objects.filter(email=admin_email).exists():
                admin_user = User.objects.create_superuser(
                    email=admin_email,
                    password=admin_password,
                    name='Admin User',
                    team='PROJECT_MANAGER'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created admin user: {admin_email}')
                )
            else:
                # Update existing admin user password
                admin_user = User.objects.get(email=admin_email)
                admin_user.set_password(admin_password)
                admin_user.is_staff = True
                admin_user.is_superuser = True
                admin_user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Updated admin user password: {admin_email}')
                )

            # Create test users
            test_users = [
                {'email': 'faris@example.com', 'name': 'Faris Mullen', 'team': 'PROJECT_MANAGER'},
                {'email': 'syam@example.com', 'name': 'Syam Murali', 'team': 'PROJECT_MANAGER'},
                {'email': 'thabsheer@example.com', 'name': 'Thabsheer', 'team': 'TECH'},
                {'email': 'vivek@example.com', 'name': 'Vivek Purayath', 'team': 'TECH'},
                {'email': 'jaseel@example.com', 'name': 'Jaseel', 'team': 'TECH'},
                {'email': 'sreehari@example.com', 'name': 'Sreehari', 'team': 'TECH'},
                {'email': 'dileep@example.com', 'name': 'Dileep Krishnan', 'team': 'TECH'},
                {'email': 'febi@example.com', 'name': 'Febi Wilson Vazhakkan', 'team': 'TECH'},
                {'email': 'vyshak@example.com', 'name': 'Vyshak PK', 'team': 'TECH'},
            ]

            for user_data in test_users:
                if not User.objects.filter(email=user_data['email']).exists():
                    user = User.objects.create_user(
                        email=user_data['email'],
                        password='password123',
                        name=user_data['name'],
                        team=user_data['team']
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Created user: {user_data["name"]} ({user_data["email"]})')
                    )
                else:
                    # Update existing user password
                    user = User.objects.get(email=user_data['email'])
                    user.set_password('password123')
                    user.name = user_data['name']
                    user.team = user_data['team']
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated user: {user_data["name"]} ({user_data["email"]})')
                    )

        self.stdout.write(
            self.style.SUCCESS('User setup completed successfully!')
        )
