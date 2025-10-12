from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Check and create users from the provided list'

    def handle(self, *args, **options):
        # Users from the image
        users_data = [
            {"name": "Admin User", "email": "admin@example.com", "password": "admin123"},
            {"name": "Faris Mullen", "email": "farismullen93@gmail.com", "password": "faris123"},
            {"name": "Syam Murali", "email": "muralisyam1@gmail.com", "password": "syam123"},
            {"name": "Dileep Krishnan", "email": "dileepkrishnan92@gmail.com", "password": "dileep123"},
            {"name": "Febi Wilson Vazhakkan", "email": "febiwilsonvazhakkan@gmail.com", "password": "febi123"},
            {"name": "Sreehari", "email": "grytt.sreehari@gmail.com", "password": "sreehari123"},
            {"name": "Thabsheer", "email": "thabsheeron@gmail.com", "password": "thabsheer123"},
            {"name": "Vyshak PK", "email": "vyshakpk10@gmail.com", "password": "vyshak123"},
            {"name": "Vivek Purayath", "email": "purayathvivek@gmail.com", "password": "vivek123"},
            {"name": "Jaseel", "email": "jasa542000@gmail.com", "password": "jaseel123"},
        ]

        self.stdout.write("🔍 Checking existing users...")
        existing_users = User.objects.all()
        self.stdout.write(f"Found {existing_users.count()} existing users:")

        for user in existing_users:
            self.stdout.write(f"  - {user.name} ({user.email})")

        self.stdout.write("\n📝 Checking and creating missing users...")

        created_count = 0
        for user_data in users_data:
            email = user_data["email"]
            
            # Check if user exists
            if User.objects.filter(email=email).exists():
                self.stdout.write(f"  ✅ {user_data['name']} already exists")
            else:
                # Create new user
                user = User.objects.create_user(
                    email=email,
                    name=user_data["name"],
                    password=user_data["password"],
                    is_active=True,
                    is_staff=(email == "admin@example.com"),  # Make admin user staff
                    is_superuser=(email == "admin@example.com")  # Make admin user superuser
                )
                self.stdout.write(f"  ➕ Created: {user_data['name']} ({email})")
                created_count += 1

        self.stdout.write(f"\n🎉 Process complete! Created {created_count} new users.")
        self.stdout.write(f"📊 Total users in database: {User.objects.count()}")

        # Show all users
        self.stdout.write("\n👥 All users:")
        for user in User.objects.all():
            role = "Admin" if user.is_superuser else "Member"
            self.stdout.write(f"  - {user.name} ({user.email}) - {role}")
