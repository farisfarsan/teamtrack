from django.core.management.base import BaseCommand
from django.db.models import Count
from tasks.models import Task
from accounts.models import User

class Command(BaseCommand):
    help = 'Check and fix task data issues'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Checking task data issues...')
        
        # Check all tasks
        all_tasks = Task.objects.all()
        self.stdout.write(f'\n📊 Total tasks in database: {all_tasks.count()}')
        
        # Show all tasks with details
        self.stdout.write('\n📋 All Tasks:')
        self.stdout.write('-' * 80)
        for task in all_tasks:
            self.stdout.write(f'ID: {task.id} | Title: {task.title} | Assigned to: {task.assigned_to.name} ({task.assigned_to.get_team_display()}) | Status: {task.status}')
        
        # Check team-wise task distribution
        self.stdout.write('\n🏢 Team-wise Task Distribution:')
        self.stdout.write('-' * 80)
        
        for team_code, team_name in User.TEAMS:
            team_users = User.objects.filter(team=team_code)
            team_tasks = Task.objects.filter(assigned_to__in=team_users)
            
            self.stdout.write(f'{team_name}:')
            self.stdout.write(f'  - Team Members: {team_users.count()}')
            self.stdout.write(f'  - Total Tasks: {team_tasks.count()}')
            self.stdout.write(f'  - Pending: {team_tasks.filter(status="PENDING").count()}')
            self.stdout.write(f'  - Completed: {team_tasks.filter(status="COMPLETED").count()}')
            
            if team_tasks.exists():
                self.stdout.write(f'  - Tasks:')
                for task in team_tasks:
                    self.stdout.write(f'    * {task.title} (Assigned to: {task.assigned_to.name})')
            self.stdout.write('')
        
        # Check for orphaned tasks (tasks assigned to users who don't exist)
        orphaned_tasks = Task.objects.filter(assigned_to__isnull=True)
        if orphaned_tasks.exists():
            self.stdout.write(f'⚠️  Found {orphaned_tasks.count()} orphaned tasks (no assigned user)')
            for task in orphaned_tasks:
                self.stdout.write(f'  - Task ID {task.id}: {task.title}')
        
        # Check for tasks with invalid team assignments
        invalid_team_tasks = Task.objects.exclude(team__in=[choice[0] for choice in Task.TEAMS])
        if invalid_team_tasks.exists():
            self.stdout.write(f'⚠️  Found {invalid_team_tasks.count()} tasks with invalid team assignments')
            for task in invalid_team_tasks:
                self.stdout.write(f'  - Task ID {task.id}: {task.title} (Team: {task.team})')
        
        self.stdout.write('\n✅ Task data check completed!')
