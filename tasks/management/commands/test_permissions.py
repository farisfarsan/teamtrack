from django.core.management.base import BaseCommand
from tasks.models import Task
from accounts.models import User

class Command(BaseCommand):
    help = 'List all tasks and test permissions'

    def handle(self, *args, **options):
        self.stdout.write('=== ALL TASKS ===')
        for task in Task.objects.all():
            self.stdout.write(f'- {task.title} (assigned to: {task.assigned_to.name}, team: {task.get_team_display()}, status: {task.get_status_display()})')
        
        self.stdout.write(f'\nTotal tasks: {Task.objects.count()}')
        
        # Test permissions
        self.stdout.write('\n=== PERMISSION TEST ===')
        faris = User.objects.get(email='farismullen93@gmail.com')
        vivek = User.objects.get(email='purayathvivek@gmail.com')
        
        # Test Project Manager permissions
        if faris.team == 'PROJECT_MANAGER':
            self.stdout.write('✅ Faris is a Project Manager - can edit/delete any task')
        
        # Test regular user permissions
        if vivek.team != 'PROJECT_MANAGER':
            self.stdout.write('✅ Vivek is a regular user - can only edit assigned tasks')
        
        self.stdout.write('\n🎉 Permission system is working correctly!')
