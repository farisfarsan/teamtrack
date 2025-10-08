from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Ensure all required users exist with correct credentials'

    def handle(self, *args, **options):
        self.stdout.write('Starting user creation/update process...')
        
        # Users to create/update
        users_data = [
            {
                'email': 'admin@example.com',
                'name': 'Admin User',
                'password': 'admin123',
                'team': 'PROJECT_MANAGER',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'email': 'farismullen93@gmail.com',
                'name': 'Faris',
                'password': 'faris123',
                'team': 'PROJECT_MANAGER',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'email': 'thabsheeron@gmail.com',
                'name': 'Thabsheer',
                'password': 'thabsheer123',
                'team': 'TECH'
            },
            {
                'email': 'purayathvivek@gmail.com',
                'name': 'Vivek',
                'password': 'vivek123',
                'team': 'PRODUCT_MANAGEMENT'
            },
            {
                'email': 'jasa542000@gmail.com',
                'name': 'Jaseel',
                'password': 'jaseel123',
                'team': 'MARKETING'
            },
            {
                'email': 'grytt.sreehari@gmail.com',
                'name': 'Sreehari',
                'password': 'sreehari123',
                'team': 'TECH'
            },
            {
                'email': 'muralisyam1@gmail.com',
                'name': 'Syam Murali',
                'password': 'syam123',
                'team': 'TECH'
            },
            {
                'email': 'vyshak@example.com',
                'name': 'Vyshak',
                'password': 'vyshak123',
                'team': 'TECH'
            },
            {
                'email': 'dileep@example.com',
                'name': 'Dileep',
                'password': 'dileep123',
                'team': 'TECH'
            }
        ]

        created_count = 0
        updated_count = 0
        error_count = 0

        for user_data in users_data:
            email = user_data['email']
            
            try:
                user = User.objects.get(email=email)
                # Update existing user
                user.name = user_data['name']
                user.team = user_data['team']
                user.is_staff = user_data.get('is_staff', False)
                user.is_superuser = user_data.get('is_superuser', False)
                user.set_password(user_data['password'])
                user.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Updated user: {email} ({user_data["name"]})')
                )
            except User.DoesNotExist:
                try:
                    # Create new user
                    user = User.objects.create_user(
                        email=email,
                        name=user_data['name'],
                        password=user_data['password'],
                        team=user_data['team']
                    )
                    if user_data.get('is_staff', False):
                        user.is_staff = True
                    if user_data.get('is_superuser', False):
                        user.is_superuser = True
                    user.save()
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Created user: {email} ({user_data["name"]})')
                    )
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'❌ Error creating user {email}: {str(e)}')
                    )
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'❌ Error updating user {email}: {str(e)}')
                )

        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS(
                f'📊 SUMMARY: Created {created_count} users, Updated {updated_count} users, Errors: {error_count}'
            )
        )

        # List all users with their details
        self.stdout.write('\n📋 ALL USERS IN DATABASE:')
        self.stdout.write('-' * 80)
        for user in User.objects.all().order_by('email'):
            role = "Admin" if user.is_superuser else "Project Manager" if user.team == 'PROJECT_MANAGER' else user.get_team_display()
            self.stdout.write(f'📧 {user.email:<30} | 👤 {user.name:<15} | 🏢 {role:<20} | ✅ Active: {user.is_active}')
        
        self.stdout.write('\n🔐 LOGIN CREDENTIALS:')
        self.stdout.write('-' * 80)
        for user_data in users_data:
            self.stdout.write(f'📧 Email: {user_data["email"]:<30} | 🔑 Password: {user_data["password"]}')
        
        self.stdout.write('\n🌐 APPLICATION URL: https://teamtrack-1.onrender.com')
        self.stdout.write('🎯 Ready for login!')
