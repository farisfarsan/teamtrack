from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Create real users from the provided list'

    def handle(self, *args, **options):
        users_data = [
            ('farismullen93@gmail.com', 'faris123', 'Faris Mullen', 'TECH'),
            ('muralisyam1@gmail.com', 'syam123', 'Syam Murali', 'TECH'),
            ('dileepkrishnan92@gmail.com', 'dileep123', 'Dileep Krishnan', 'DESIGN'),
            ('febiwilsonvazhakkan@gmail.com', 'febi123', 'Febi Wilson Vazhakkan', 'DESIGN'),
            ('grytt.sreehari@gmail.com', 'sreehari123', 'Sreehari', 'MARKETING'),
            ('thabsheeron@gmail.com', 'thabsheer123', 'Thabsheer', 'MARKETING'),
            ('vyshakpk10@gmail.com', 'vyshak123', 'Vyshak PK', 'TECH'),
            ('purayathvivek@gmail.com', 'vivek123', 'Vivek Purayath', 'TECH'),
            ('jasa542000@gmail.com', 'jaseel123', 'Jaseel', 'MARKETING'),
        ]
        
        created_count = 0
        for email, password, name, team in users_data:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'name': name, 'team': team}
            )
            if created:
                user.set_password(password)
                user.save()
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {name} ({email})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User already exists: {name} ({email})')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new users')
        )
