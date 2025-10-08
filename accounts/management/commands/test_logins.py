from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from accounts.models import User

class Command(BaseCommand):
    help = 'Test login for all users to verify credentials work'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Testing login credentials for all users...')
        self.stdout.write('=' * 60)
        
        # Test credentials
        test_users = [
            {'email': 'admin@example.com', 'password': 'admin123', 'name': 'Admin User'},
            {'email': 'farismullen93@gmail.com', 'password': 'faris123', 'name': 'Faris'},
            {'email': 'thabsheeron@gmail.com', 'password': 'thabsheer123', 'name': 'Thabsheer'},
            {'email': 'purayathvivek@gmail.com', 'password': 'vivek123', 'name': 'Vivek'},
            {'email': 'jasa542000@gmail.com', 'password': 'jaseel123', 'name': 'Jaseel'},
            {'email': 'grytt.sreehari@gmail.com', 'password': 'sreehari123', 'name': 'Sreehari'},
            {'email': 'muralisyam1@gmail.com', 'password': 'syam123', 'name': 'Syam Murali'},
            {'email': 'vyshak@example.com', 'password': 'vyshak123', 'name': 'Vyshak'},
            {'email': 'dileep@example.com', 'password': 'dileep123', 'name': 'Dileep'},
        ]
        
        success_count = 0
        fail_count = 0
        
        for user_data in test_users:
            email = user_data['email']
            password = user_data['password']
            name = user_data['name']
            
            # Test authentication
            user = authenticate(email=email, password=password)
            
            if user:
                success_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ {name:<15} | {email:<30} | Login: SUCCESS')
                )
            else:
                fail_count += 1
                self.stdout.write(
                    self.style.ERROR(f'❌ {name:<15} | {email:<30} | Login: FAILED')
                )
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(
            self.style.SUCCESS(f'📊 LOGIN TEST RESULTS: {success_count} SUCCESS, {fail_count} FAILED')
        )
        
        if fail_count == 0:
            self.stdout.write(self.style.SUCCESS('🎉 All users can login successfully!'))
        else:
            self.stdout.write(self.style.ERROR(f'⚠️  {fail_count} users have login issues'))
        
        self.stdout.write('\n🌐 Application URL: https://teamtrack-1.onrender.com')
        self.stdout.write('🔐 Ready for team login!')
