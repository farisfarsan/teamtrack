from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Create users for PythonAnywhere deployment'

    def handle(self, *args, **options):
        self.stdout.write("👥 Setting up users for PythonAnywhere...")
        
        # Users with their credentials
        users_data = [
            {'email': 'admin@example.com', 'name': 'Admin User', 'team': 'PROJECT_MANAGER', 'password': 'admin123', 'is_admin': True},
            {'email': 'farismullen93@gmail.com', 'name': 'Faris Mullen', 'team': 'PROJECT_MANAGER', 'password': 'faris123', 'is_admin': False},
            {'email': 'muralisyam1@gmail.com', 'name': 'Syam Murali', 'team': 'DESIGN', 'password': 'syam123', 'is_admin': False},
            {'email': 'dileepkrishnan92@gmail.com', 'name': 'Dileep Krishnan', 'team': 'DESIGN', 'password': 'dileep123', 'is_admin': False},
            {'email': 'febiwilsonvazhakkan@gmail.com', 'name': 'Febi Wilson Vazhakkan', 'team': 'DESIGN', 'password': 'febi123', 'is_admin': False},
            {'email': 'grytt.sreehari@gmail.com', 'name': 'Sreehari', 'team': 'TECH', 'password': 'sreehari123', 'is_admin': False},
            {'email': 'thabsheeron@gmail.com', 'name': 'Thabsheer', 'team': 'TECH', 'password': 'thabsheer123', 'is_admin': False},
            {'email': 'vyshakpk10@gmail.com', 'name': 'Vyshak PK', 'team': 'TECH', 'password': 'vyshak123', 'is_admin': False},
            {'email': 'purayathvivek@gmail.com', 'name': 'Vivek Purayath', 'team': 'PRODUCT_MANAGEMENT', 'password': 'vivek123', 'is_admin': False},
            {'email': 'jasa542000@gmail.com', 'name': 'Jaseel', 'team': 'MARKETING', 'password': 'jaseel123', 'is_admin': False},
        ]

        created_count = 0
        updated_count = 0
        
        for user_data in users_data:
            email = user_data['email']
            
            if User.objects.filter(email=email).exists():
                # Update existing user
                user = User.objects.get(email=email)
                user.set_password(user_data['password'])
                user.name = user_data['name']
                user.team = user_data['team']
                user.is_active = True
                
                if user_data.get('is_admin', False):
                    user.is_superuser = True
                    user.is_staff = True
                
                user.save()
                self.stdout.write(self.style.SUCCESS(f"✅ Updated: {user_data['name']} ({email})"))
                updated_count += 1
            else:
                # Create new user
                user = User.objects.create_user(
                    email=email,
                    password=user_data['password'],
                    name=user_data['name'],
                    team=user_data['team']
                )
                user.is_active = True
                
                if user_data.get('is_admin', False):
                    user.is_superuser = True
                    user.is_staff = True
                
                user.save()
                self.stdout.write(self.style.SUCCESS(f"➕ Created: {user_data['name']} ({email})"))
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"🎉 User setup complete! Created: {created_count}, Updated: {updated_count}"))
        
        # Test admin login
        from django.contrib.auth import authenticate
        admin_user = authenticate(email="admin@example.com", password="admin123")
        if admin_user:
            self.stdout.write(self.style.SUCCESS("✅ Admin login test: PASSED"))
        else:
            self.stdout.write(self.style.ERROR("❌ Admin login test: FAILED"))
        
        # Show all users
        self.stdout.write("\n👥 All users:")
        for user in User.objects.all():
            role = "Admin" if user.is_superuser else "Member"
            self.stdout.write(f"  - {user.name} ({user.email}) - {role}")
