from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Clean up fake users and update team assignments for production'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Remove all fake users with @example.com emails
            fake_users = User.objects.filter(email__endswith='@example.com')
            fake_count = fake_users.count()
            
            if fake_count > 0:
                self.stdout.write(f'Found {fake_count} fake users to remove:')
                for user in fake_users:
                    self.stdout.write(f'  - {user.name}: {user.email}')
                
                fake_users.delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Removed {fake_count} fake users')
                )
            else:
                self.stdout.write('No fake users found')

            # Update team assignments for existing users
            team_updates = [
                ('farismullen93@gmail.com', 'PROJECT_MANAGER'),
                ('muralisyam1@gmail.com', 'DESIGN'),
                ('dileepkrishnan92@gmail.com', 'DESIGN'),
                ('febiwilsonvazhakkan@gmail.com', 'DESIGN'),
                ('grytt.sreehari@gmail.com', 'TECH'),
                ('thabsheeron@gmail.com', 'TECH'),
                ('vyshakpk10@gmail.com', 'TECH'),
                ('purayathvivek@gmail.com', 'PRODUCT_MANAGEMENT'),
                ('jasa542000@gmail.com', 'MARKETING'),
            ]

            updated_count = 0
            for email, team in team_updates:
                try:
                    user = User.objects.get(email=email)
                    old_team = user.team
                    user.team = team
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated {user.name}: {old_team} → {team}')
                    )
                    updated_count += 1
                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'User not found: {email}')
                    )

            # Grant admin privileges to Syam Murali
            try:
                syam = User.objects.get(email='muralisyam1@gmail.com')
                syam.is_superuser = True
                syam.is_staff = True
                syam.save()
                self.stdout.write(
                    self.style.SUCCESS('Granted admin privileges to Syam Murali')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING('Syam Murali not found')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Cleanup completed! Updated {updated_count} users')
        )
