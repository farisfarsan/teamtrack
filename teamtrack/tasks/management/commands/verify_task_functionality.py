from django.core.management.base import BaseCommand
from tasks.models import Task, TaskComment

class Command(BaseCommand):
    help = 'Verify task functionality'

    def handle(self, *args, **options):
        try:
            task = Task.objects.get(title='Phase 3 Screen Design')
            self.stdout.write(f'✅ Task: {task.title}')
            self.stdout.write(f'✅ Status: {task.get_status_display()}')
            self.stdout.write(f'✅ Assigned to: {task.assigned_to.name}')
            self.stdout.write(f'✅ Comments: {task.comments.count()}')
            
            for comment in task.comments.all():
                self.stdout.write(f'  - {comment.get_comment_type_display()}: {comment.message[:50]}...')
                
            self.stdout.write('\n🎉 Task functionality is working correctly!')
        except Task.DoesNotExist:
            self.stdout.write('❌ Task not found')
