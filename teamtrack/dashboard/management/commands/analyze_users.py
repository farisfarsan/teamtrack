from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Analyze user counts and team distribution'

    def handle(self, *args, **options):
        self.stdout.write('📊 User Analysis Report')
        self.stdout.write('=' * 50)
        
        # Total users
        total_users = User.objects.count()
        self.stdout.write(f'Total Users: {total_users}')
        
        # Active users
        active_users = User.objects.filter(is_active=True).count()
        self.stdout.write(f'Active Users: {active_users}')
        
        # Team members (excluding PROJECT_MANAGER)
        team_members = User.objects.filter(is_active=True).exclude(team='PROJECT_MANAGER').count()
        self.stdout.write(f'Team Members (excluding PROJECT_MANAGER): {team_members}')
        
        self.stdout.write('\n📋 Team Distribution:')
        self.stdout.write('-' * 30)
        
        for team_code, team_name in User.TEAMS:
            count = User.objects.filter(team=team_code, is_active=True).count()
            self.stdout.write(f'{team_name}: {count} users')
            
        self.stdout.write('\n👥 All Users Details:')
        self.stdout.write('-' * 30)
        
        for user in User.objects.filter(is_active=True):
            status = "Active" if user.is_active else "Inactive"
            self.stdout.write(f'- {user.name} ({user.email}) - {user.get_team_display()} - {status}')
            
        self.stdout.write('\n🔍 Analysis:')
        self.stdout.write('-' * 30)
        self.stdout.write(f'Active Users (10): All users with is_active=True')
        self.stdout.write(f'Team Members (7): Active users excluding PROJECT_MANAGER team')
        
        # Check PROJECT_MANAGER count
        pm_count = User.objects.filter(team='PROJECT_MANAGER', is_active=True).count()
        self.stdout.write(f'Project Managers: {pm_count}')
        self.stdout.write(f'Calculation: {active_users} - {pm_count} = {team_members}')
