from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class Command(BaseCommand):
    help = 'Create user profiles for team members'

    def handle(self, *args, **options):
        # User data to create
        users_data = [
            {
                'email': 'thabsheeron@gmail.com',
                'password': 'thabsheer123',
                'name': 'Thabsheer',
                'team': 'TECH'
            },
            {
                'email': 'purayathvivek@gmail.com',
                'password': 'vivek123',
                'name': 'Vivek Purayath',
                'team': 'PRODUCT_MANAGEMENT'
            },
            {
                'email': 'jasa542000@gmail.com',
                'password': 'jaseel123',
                'name': 'Jaseel',
                'team': 'MARKETING'
            },
            {
                'email': 'grytt.sreehari@gmail.com',
                'password': 'sreehari123',
                'name': 'Sreehari',
                'team': 'TECH'
            }
        ]

        # Update existing user
        existing_user_email = 'muralisyam1@gmail.com'
        new_password = 'syam123'
        new_name = 'Syam Murali'

        # Create new users
        created_count = 0
        for user_data in users_data:
            try:
                user, created = User.objects.get_or_create(
                    email=user_data['email'],
                    defaults={
                        'name': user_data['name'],
                        'team': user_data['team']
                    }
                )
                
                if created:
                    user.set_password(user_data['password'])
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Created user: {user.name} ({user.email}) - {user.get_team_display()}')
                    )
                    created_count += 1
                else:
                    # Update password if user exists
                    user.set_password(user_data['password'])
                    user.name = user_data['name']
                    user.team = user_data['team']
                    user.save()
                    self.stdout.write(
                        self.style.WARNING(f'🔄 Updated user: {user.name} ({user.email}) - {user.get_team_display()}')
                    )
                    
            except IntegrityError as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error creating user {user_data["email"]}: {str(e)}')
                )

        # Update existing user
        try:
            existing_user = User.objects.get(email=existing_user_email)
            existing_user.set_password(new_password)
            existing_user.name = new_name
            existing_user.save()
            self.stdout.write(
                self.style.SUCCESS(f'✅ Updated existing user: {existing_user.name} ({existing_user.email})')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ User {existing_user_email} not found')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Successfully processed {created_count} new users and updated 1 existing user!')
        )
        
        # Display all users
        self.stdout.write('\n📋 All Users in the system:')
        self.stdout.write('-' * 50)
        for user in User.objects.all().order_by('team', 'name'):
            self.stdout.write(f'{user.name} ({user.email}) - {user.get_team_display()}')
