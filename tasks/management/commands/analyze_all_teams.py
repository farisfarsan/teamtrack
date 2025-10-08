from django.core.management.base import BaseCommand
from django.db.models import Count, Q
from tasks.models import Task
from accounts.models import User
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Comprehensive team and task data analysis'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Comprehensive Team & Task Analysis')
        self.stdout.write('=' * 60)
        
        # Clear cache first
        cache.clear()
        self.stdout.write('✅ Cache cleared')
        
        # Check all users
        self.stdout.write(f'\n👥 USER ANALYSIS:')
        self.stdout.write('-' * 40)
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        self.stdout.write(f'Total Users: {total_users}')
        self.stdout.write(f'Active Users: {active_users}')
        
        # Show all users by team
        for team_code, team_name in User.TEAMS:
            team_users = User.objects.filter(team=team_code)
            if team_users.exists():
                self.stdout.write(f'\n{team_name} Team ({team_code}):')
                for user in team_users:
                    status = "Active" if user.is_active else "Inactive"
                    role = "Admin" if user.is_superuser else "Manager" if user.is_staff else "Member"
                    self.stdout.write(f'  - {user.name} ({user.email}) - {status} - {role}')
            else:
                self.stdout.write(f'\n{team_name} Team ({team_code}): No members')
        
        # Check all tasks
        self.stdout.write(f'\n📋 TASK ANALYSIS:')
        self.stdout.write('-' * 40)
        total_tasks = Task.objects.count()
        self.stdout.write(f'Total Tasks: {total_tasks}')
        
        if total_tasks > 0:
            # Show all tasks with details
            self.stdout.write('\nAll Tasks:')
            for task in Task.objects.all():
                self.stdout.write(f'  ID: {task.id}')
                self.stdout.write(f'  Title: {task.title}')
                self.stdout.write(f'  Description: {task.description[:50]}...' if task.description else '  Description: None')
                self.stdout.write(f'  Assigned to: {task.assigned_to.name} ({task.assigned_to.get_team_display()})')
                self.stdout.write(f'  Assigned by: {task.assigned_by.name if task.assigned_by else "Unknown"}')
                self.stdout.write(f'  Team: {task.get_team_display()}')
                self.stdout.write(f'  Status: {task.get_status_display()}')
                self.stdout.write(f'  Priority: {task.get_priority_display()}')
                self.stdout.write(f'  Due Date: {task.due_date}')
                self.stdout.write(f'  Created: {task.created_at}')
                self.stdout.write(f'  Updated: {task.updated_at}')
                self.stdout.write('  ' + '-' * 30)
        else:
            self.stdout.write('No tasks found in database')
        
        # Team-wise analysis
        self.stdout.write(f'\n🏢 TEAM-WISE ANALYSIS:')
        self.stdout.write('-' * 40)
        
        for team_code, team_name in User.TEAMS:
            team_users = User.objects.filter(team=team_code)
            team_tasks = Task.objects.filter(assigned_to__in=team_users)
            
            self.stdout.write(f'\n{team_name} Team:')
            self.stdout.write(f'  Members: {team_users.count()}')
            self.stdout.write(f'  Total Tasks: {team_tasks.count()}')
            self.stdout.write(f'  Pending: {team_tasks.filter(status="PENDING").count()}')
            self.stdout.write(f'  In Progress: {team_tasks.filter(status="IN_PROGRESS").count()}')
            self.stdout.write(f'  Completed: {team_tasks.filter(status="COMPLETED").count()}')
            self.stdout.write(f'  Review: {team_tasks.filter(status="REVIEW").count()}')
            self.stdout.write(f'  Blocked: {team_tasks.filter(status="BLOCKED").count()}')
            
            # Check for tasks assigned by team members
            tasks_assigned_by_team = Task.objects.filter(assigned_by__in=team_users)
            self.stdout.write(f'  Tasks Assigned by Team: {tasks_assigned_by_team.count()}')
            
            # Show specific tasks if any
            if team_tasks.exists():
                self.stdout.write(f'  Task Details:')
                for task in team_tasks:
                    self.stdout.write(f'    - {task.title} (Status: {task.status})')
        
        # Check for data inconsistencies
        self.stdout.write(f'\n🔍 DATA CONSISTENCY CHECK:')
        self.stdout.write('-' * 40)
        
        # Check for orphaned tasks
        orphaned_tasks = Task.objects.filter(assigned_to__isnull=True)
        if orphaned_tasks.exists():
            self.stdout.write(f'⚠️  Orphaned Tasks: {orphaned_tasks.count()}')
            for task in orphaned_tasks:
                self.stdout.write(f'  - Task ID {task.id}: {task.title}')
        
        # Check for tasks with invalid team assignments
        valid_teams = [choice[0] for choice in Task.TEAMS]
        invalid_team_tasks = Task.objects.exclude(team__in=valid_teams)
        if invalid_team_tasks.exists():
            self.stdout.write(f'⚠️  Invalid Team Tasks: {invalid_team_tasks.count()}')
            for task in invalid_team_tasks:
                self.stdout.write(f'  - Task ID {task.id}: {task.title} (Team: {task.team})')
        
        # Check for tasks assigned to inactive users
        inactive_user_tasks = Task.objects.filter(assigned_to__is_active=False)
        if inactive_user_tasks.exists():
            self.stdout.write(f'⚠️  Tasks Assigned to Inactive Users: {inactive_user_tasks.count()}')
            for task in inactive_user_tasks:
                self.stdout.write(f'  - Task ID {task.id}: {task.title} (User: {task.assigned_to.name})')
        
        # Check for tasks with missing assigned_by
        missing_assigned_by = Task.objects.filter(assigned_by__isnull=True)
        if missing_assigned_by.exists():
            self.stdout.write(f'⚠️  Tasks with Missing Assigned By: {missing_assigned_by.count()}')
            for task in missing_assigned_by:
                self.stdout.write(f'  - Task ID {task.id}: {task.title}')
        
        self.stdout.write(f'\n✅ Analysis completed!')
