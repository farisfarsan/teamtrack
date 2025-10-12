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

            # Create test users with correct emails and passwords
            test_users = [
                {'email': 'farismullen93@gmail.com', 'name': 'Faris Mullen', 'team': 'PROJECT_MANAGER', 'password': 'faris123'},
                {'email': 'muralisyam1@gmail.com', 'name': 'Syam Murali', 'team': 'PROJECT_MANAGER', 'password': 'syam123'},
                {'email': 'thabsheeron@gmail.com', 'name': 'Thabsheer', 'team': 'TECH', 'password': 'thabsheer123'},
                {'email': 'purayathvivek@gmail.com', 'name': 'Vivek Purayath', 'team': 'PRODUCT_MANAGEMENT', 'password': 'vivek123'},
                {'email': 'jasa542000@gmail.com', 'name': 'Jaseel', 'team': 'MARKETING', 'password': 'jaseel123'},
                {'email': 'grytt.sreehari@gmail.com', 'name': 'Sreehari', 'team': 'TECH', 'password': 'sreehari123'},
                {'email': 'dileepkrishnan92@gmail.com', 'name': 'Dileep Krishnan', 'team': 'DESIGN', 'password': 'dileep123'},
                {'email': 'febiwilsonvazhakkan@gmail.com', 'name': 'Febi Wilson Vazhakkan', 'team': 'DESIGN', 'password': 'febi123'},
                {'email': 'vyshakpk10@gmail.com', 'name': 'Vyshak PK', 'team': 'TECH', 'password': 'vyshak123'},
                {'email': 'test@example.com', 'name': 'Test User', 'team': 'TECH', 'password': 'test123'},
            ]

            for user_data in test_users:
                if not User.objects.filter(email=user_data['email']).exists():
                    user = User.objects.create_user(
                        email=user_data['email'],
                        password=user_data['password'],
                        name=user_data['name'],
                        team=user_data['team']
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Created user: {user_data["name"]} ({user_data["email"]})')
                    )
                else:
                    # Update existing user password
                    user = User.objects.get(email=user_data['email'])
                    user.set_password(user_data['password'])
                    user.name = user_data['name']
                    user.team = user_data['team']
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated user: {user_data["name"]} ({user_data["email"]})')
                    )

        self.stdout.write(
            self.style.SUCCESS('User setup completed successfully!')
        )
