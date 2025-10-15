[33mcommit 28a48682de81430eeaacbdfc67cf147196295108[m
Author: faris <farismullen93@example.com>
Date:   Mon Oct 13 19:22:35 2025 +0530

    Fix production database: remove fake users, update team assignments, grant admin to Syam

[1mdiff --git a/build.sh b/build.sh[m
[1mindex 069f434..ab8ae10 100644[m
[1m--- a/build.sh[m
[1m+++ b/build.sh[m
[36m@@ -14,6 +14,9 @@[m [mpython manage.py collectstatic --noinput --settings=settings_render[m
 # Run migrations[m
 python manage.py migrate --settings=settings_render[m
 [m
[32m+[m[32m# Clean up fake users and update team assignments[m
[32m+[m[32mpython manage.py cleanup_fake_users --settings=settings_render[m
[32m+[m
 # Create users for production[m
 python manage.py setup_render_users --settings=settings_render[m
 [m
[1mdiff --git a/teamtrack/accounts/management/commands/cleanup_fake_users.py b/teamtrack/accounts/management/commands/cleanup_fake_users.py[m
[1mnew file mode 100644[m
[1mindex 0000000..2db1c14[m
[1m--- /dev/null[m
[1m+++ b/teamtrack/accounts/management/commands/cleanup_fake_users.py[m
[36m@@ -0,0 +1,73 @@[m
[32m+[m[32mfrom django.core.management.base import BaseCommand[m
[32m+[m[32mfrom django.contrib.auth import get_user_model[m
[32m+[m[32mfrom django.db import transaction[m
[32m+[m
[32m+[m[32mUser = get_user_model()[m
[32m+[m
[32m+[m[32mclass Command(BaseCommand):[m
[32m+[m[32m    help = 'Clean up fake users and update team assignments for production'[m
[32m+[m
[32m+[m[32m    def handle(self, *args, **options):[m
[32m+[m[32m        with transaction.atomic():[m
[32m+[m[32m            # Remove all fake users with @example.com emails[m
[32m+[m[32m            fake_users = User.objects.filter(email__endswith='@example.com')[m
[32m+[m[32m            fake_count = fake_users.count()[m
[32m+[m[41m            [m
[32m+[m[32m            if fake_count > 0:[m
[32m+[m[32m                self.stdout.write(f'Found {fake_count} fake users to remove:')[m
[32m+[m[32m                for user in fake_users:[m
[32m+[m[32m                    self.stdout.write(f'  - {user.name}: {user.email}')[m
[32m+[m[41m                [m
[32m+[m[32m                fake_users.delete()[m
[32m+[m[32m                self.stdout.write([m
[32m+[m[32m                    self.style.SUCCESS(f'Removed {fake_count} fake users')[m
[32m+[m[32m                )[m
[32m+[m[32m            else:[m
[32m+[m[32m                self.stdout.write('No fake users found')[m
[32m+[m
[32m+[m[32m            # Update team assignments for existing users[m
[32m+[m[32m            team_updates = [[m
[32m+[m[32m                ('farismullen93@gmail.com', 'PROJECT_MANAGER'),[m
[32m+[m[32m                ('muralisyam1@gmail.com', 'DESIGN'),[m
[32m+[m[32m                ('dileepkrishnan92@gmail.com', 'DESIGN'),[m
[32m+[m[32m                ('febiwilsonvazhakkan@gmail.com', 'DESIGN'),[m
[32m+[m[32m                ('grytt.sreehari@gmail.com', 'TECH'),[m
[32m+[m[32m                ('thabsheeron@gmail.com', 'TECH'),[m
[32m+[m[32m                ('vyshakpk10@gmail.com', 'TECH'),[m
[32m+[m[32m                ('purayathvivek@gmail.com', 'PRODUCT_MANAGEMENT'),[m
[32m+[m[32m                ('jasa542000@gmail.com', 'MARKETING'),[m
[32m+[m[32m            ][m
[32m+[m
[32m+[m[32m            updated_count = 0[m
[32m+[m[32m            for email, team in team_updates:[m
[32m+[m[32m                try:[m
[32m+[m[32m                    user = User.objects.get(email=email)[m
[32m+[m[32m                    old_team = user.team[m
[32m+[m[32m                    user.team = team[m
[32m+[m[32m                    user.save()[m
[32m+[m[32m                    self.stdout.write([m
[32m+[m[32m                        self.style.SUCCESS(f'Updated {user.name}: {old_team} → {team}')[m
[32m+[m[32m                    )[m
[32m+[m[32m                    updated_count += 1[m
[32m+[m[32m                except User.DoesNotExist:[m
[32m+[m[32m                    self.stdout.write([m
[32m+[m[32m                        self.style.WARNING(f'User not found: {email}')[m
[32m+[m[32m                    )[m
[32m+[m
[32m+[m[32m            # Grant admin privileges to Syam Murali[m
[32m+[m[32m            try:[m
[32m+[m[32m                syam = User.objects.get(email='muralisyam1@gmail.com')[m
[32m+[m[32m                syam.is_superuser = True[m
[32m+[m[32m                syam.is_staff = True[m
[32m+[m[32m                syam.save()[m
[32m+[m[32m                self.stdout.write([m
[32m+[m[32m                    self.style.SUCCESS('Granted admin privileges to Syam Murali')[m
[32m+[m[32m                )[m
[32m+[m[32m            except User.DoesNotExist:[m
[32m+[m[32m                self.stdout.write([m
[32m+[m[32m                    self.style.WARNING('Syam Murali not found')[m
[32m+[m[32m                )[m
[32m+[m
[32m+[m[32m        self.stdout.write([m
[32m+[m[32m            self.style.SUCCESS(f'Cleanup completed! Updated {updated_count} users')[m
[32m+[m[32m        )[m
[1mdiff --git a/teamtrack/accounts/management/commands/setup_render_users.py b/teamtrack/accounts/management/commands/setup_render_users.py[m
[1mindex 8f9cdb6..fdcf609 100644[m
[1m--- a/teamtrack/accounts/management/commands/setup_render_users.py[m
[1m+++ b/teamtrack/accounts/management/commands/setup_render_users.py[m
[36m@@ -34,18 +34,17 @@[m [mclass Command(BaseCommand):[m
                     self.style.SUCCESS(f'Updated admin user password: {admin_email}')[m
                 )[m
 [m
[31m-            # Create test users with correct emails and passwords[m
[32m+[m[32m            # Create users with correct emails, teams, and admin privileges[m
             test_users = [[m
[31m-                {'email': 'farismullen93@gmail.com', 'name': 'Faris Mullen', 'team': 'PROJECT_MANAGER', 'password': 'faris123'},[m
[31m-                {'email': 'muralisyam1@gmail.com', 'name': 'Syam Murali', 'team': 'PROJECT_MANAGER', 'password': 'syam123'},[m
[31m-                {'email': 'thabsheeron@gmail.com', 'name': 'Thabsheer', 'team': 'TECH', 'password': 'thabsheer123'},[m
[31m-                {'email': 'purayathvivek@gmail.com', 'name': 'Vivek Purayath', 'team': 'PRODUCT_MANAGEMENT', 'password': 'vivek123'},[m
[31m-                {'email': 'jasa542000@gmail.com', 'name': 'Jaseel', 'team': 'MARKETING', 'password': 'jaseel123'},[m
[31m-                {'email': 'grytt.sreehari@gmail.com', 'name': 'Sreehari', 'team': 'TECH', 'password': 'sreehari123'},[m
[31m-                {'email': 'dileepkrishnan92@gmail.com', 'name': 'Dileep Krishnan', 'team': 'DESIGN', 'password': 'dileep123'},[m
[31m-                {'email': 'febiwilsonvazhakkan@gmail.com', 'name': 'Febi Wilson Vazhakkan', 'team': 'DESIGN', 'password': 'febi123'},[m
[31m-                {'email': 'vyshakpk10@gmail.com', 'name': 'Vyshak PK', 'team': 'TECH', 'password': 'vyshak123'},[m
[31m-                {'email': 'test@example.com', 'name': 'Test User', 'team': 'TECH', 'password': 'test123'},[m
[32m+[m[32m                {'email': 'farismullen93@gmail.com', 'name': 'Faris Mullen', 'team': 'PROJECT_MANAGER', 'password': 'faris123', 'is_admin': False},[m
[32m+[m[32m                {'email': 'muralisyam1@gmail.com', 'name': 'Syam Murali', 'team': 'DESIGN', 'password': 'syam123', 'is_admin': True},[m
[32m+[m[32m                {'email': 'thabsheeron@gmail.com', 'name': 'Thabsheer', 'team': 'TECH', 'password': 'thabsheer123', 'is_admin': False},[m
[32m+[m[32m                {'email': 'purayathvivek@gmail.com', 'name': 'Vivek Purayath', 'team': 'PRODUCT_MANAGEMENT', 'password': 'vivek123', 'is_admin': False},[m
[32m+[m[32m                {'email': 'jasa542000@gmail.com', 'name': 'Jaseel', 'team': 'MARKETING', 'password': 'jaseel123', 'is_admin': False},[m
[32m+[m[32m                {'email': 'grytt.sreehari@gmail.com', 'name': 'Sreehari', 'team': 'TECH', 'password': 'sreehari123', 'is_admin': False},[m
[32m+[m[32m