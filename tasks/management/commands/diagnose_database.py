from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tasks.models import Task, TaskComment
from notifications.models import Notification
from django.db import connection
from django.core.cache import cache
import logging

User = get_user_model()

class Command(BaseCommand):
    help = 'Comprehensive database and task persistence diagnostics'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Comprehensive Database Diagnostics')
        self.stdout.write('=' * 50)
        
        # Database connection info
        self.stdout.write('\n🗄️  DATABASE CONNECTION:')
        self.stdout.write('-' * 30)
        db_info = connection.get_connection_params()
        self.stdout.write(f'Database: {db_info.get("database", "Unknown")}')
        self.stdout.write(f'Host: {db_info.get("host", "Unknown")}')
        self.stdout.write(f'Port: {db_info.get("port", "Unknown")}')
        
        # Test database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write('✅ Database connection: OK')
        except Exception as e:
            self.stdout.write(f'❌ Database connection error: {e}')
            return
        
        # Cache status
        self.stdout.write('\n💾 CACHE STATUS:')
        self.stdout.write('-' * 30)
        try:
            cache.set('test_key', 'test_value', 30)
            if cache.get('test_key') == 'test_value':
                self.stdout.write('✅ Cache: Working')
            else:
                self.stdout.write('❌ Cache: Not working')
        except Exception as e:
            self.stdout.write(f'❌ Cache error: {e}')
        
        # User analysis
        self.stdout.write('\n👥 USER ANALYSIS:')
        self.stdout.write('-' * 30)
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        self.stdout.write(f'Total users: {total_users}')
        self.stdout.write(f'Active users: {active_users}')
        
        # Show users by team
        for team_code, team_name in User.TEAMS:
            team_users = User.objects.filter(team=team_code, is_active=True)
            if team_users.exists():
                self.stdout.write(f'\n{team_name}:')
                for user in team_users:
                    self.stdout.write(f'  - {user.name} ({user.email})')
        
        # Task analysis
        self.stdout.write('\n📋 TASK ANALYSIS:')
        self.stdout.write('-' * 30)
        total_tasks = Task.objects.count()
        self.stdout.write(f'Total tasks: {total_tasks}')
        
        if total_tasks > 0:
            # Show all tasks with details
            for task in Task.objects.all().order_by('-created_at'):
                self.stdout.write(f'\nTask ID: {task.id}')
                self.stdout.write(f'  Title: {task.title}')
                self.stdout.write(f'  Description: {task.description[:50]}...' if task.description else '  Description: None')
                self.stdout.write(f'  Assigned to: {task.assigned_to.name} ({task.assigned_to.get_team_display()})')
                self.stdout.write(f'  Assigned by: {task.assigned_by.name if task.assigned_by else "Unknown"}')
                self.stdout.write(f'  Team: {task.get_team_display()}')
                self.stdout.write(f'  Status: {task.get_status_display()}')
                self.stdout.write(f'  Priority: {task.get_priority_display()}')
                self.stdout.write(f'  Created: {task.created_at}')
                self.stdout.write(f'  Updated: {task.updated_at}')
                
                # Check for comments
                comments = task.comments.count()
                self.stdout.write(f'  Comments: {comments}')
                
                # Check for notifications
                notifications = Notification.objects.filter(
                    message__icontains=task.title
                ).count()
                self.stdout.write(f'  Related notifications: {notifications}')
        else:
            self.stdout.write('No tasks found in database')
        
        # Team-wise task distribution
        self.stdout.write('\n🏢 TEAM-WISE TASK DISTRIBUTION:')
        self.stdout.write('-' * 30)
        for team_code, team_name in User.TEAMS:
            team_users = User.objects.filter(team=team_code, is_active=True)
            team_tasks = Task.objects.filter(assigned_to__in=team_users)
            
            self.stdout.write(f'\n{team_name}:')
            self.stdout.write(f'  Members: {team_users.count()}')
            self.stdout.write(f'  Total tasks: {team_tasks.count()}')
            self.stdout.write(f'  Pending: {team_tasks.filter(status="PENDING").count()}')
            self.stdout.write(f'  In Progress: {team_tasks.filter(status="IN_PROGRESS").count()}')
            self.stdout.write(f'  Completed: {team_tasks.filter(status="COMPLETED").count()}')
            
            if team_tasks.exists():
                self.stdout.write(f'  Task details:')
                for task in team_tasks:
                    self.stdout.write(f'    - {task.title} (Status: {task.status})')
        
        # Check for data integrity issues
        self.stdout.write('\n🔍 DATA INTEGRITY CHECK:')
        self.stdout.write('-' * 30)
        
        # Check for orphaned tasks
        orphaned_tasks = Task.objects.filter(assigned_to__isnull=True)
        if orphaned_tasks.exists():
            self.stdout.write(f'⚠️  Orphaned tasks: {orphaned_tasks.count()}')
        
        # Check for tasks with inactive users
        inactive_user_tasks = Task.objects.filter(assigned_to__is_active=False)
        if inactive_user_tasks.exists():
            self.stdout.write(f'⚠️  Tasks assigned to inactive users: {inactive_user_tasks.count()}')
        
        # Check for tasks with missing assigned_by
        missing_assigned_by = Task.objects.filter(assigned_by__isnull=True)
        if missing_assigned_by.exists():
            self.stdout.write(f'⚠️  Tasks with missing assigned_by: {missing_assigned_by.count()}')
        
        # Check for duplicate tasks
        duplicate_titles = Task.objects.values('title').annotate(
            count=Count('title')
        ).filter(count__gt=1)
        if duplicate_titles.exists():
            self.stdout.write(f'⚠️  Duplicate task titles: {duplicate_titles.count()}')
        
        self.stdout.write('\n✅ Diagnostics completed!')
