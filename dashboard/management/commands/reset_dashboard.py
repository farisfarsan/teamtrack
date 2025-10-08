from django.core.management.base import BaseCommand
from django.core.cache import cache
from tasks.models import Task
from accounts.models import User

class Command(BaseCommand):
    help = 'Clear cache and reset dashboard data'

    def handle(self, *args, **options):
        self.stdout.write('🧹 Clearing cache and resetting dashboard...')
        
        # Clear all cache
        cache.clear()
        self.stdout.write('✅ Cache cleared')
        
        # Check current task count
        task_count = Task.objects.count()
        self.stdout.write(f'📊 Current task count: {task_count}')
        
        # Check user count
        user_count = User.objects.count()
        self.stdout.write(f'👥 Current user count: {user_count}')
        
        # Show all users
        self.stdout.write('\n👥 All Users:')
        for user in User.objects.all():
            self.stdout.write(f'  - {user.name} ({user.email}) - {user.get_team_display()}')
        
        # Show all tasks
        if task_count > 0:
            self.stdout.write('\n📋 All Tasks:')
            for task in Task.objects.all():
                self.stdout.write(f'  - {task.title} (Assigned to: {task.assigned_to.name}) - {task.status}')
        else:
            self.stdout.write('\n📋 No tasks found in database')
        
        self.stdout.write('\n✅ Dashboard reset completed!')
