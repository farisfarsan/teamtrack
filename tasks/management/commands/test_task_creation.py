from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tasks.models import Task
from notifications.models import Notification
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Test task creation and persistence'

    def handle(self, *args, **options):
        self.stdout.write('🧪 Testing task creation and persistence...')
        
        # Get a project manager and a regular user
        try:
            pm = User.objects.filter(team='PROJECT_MANAGER', is_active=True).first()
            if not pm:
                self.stdout.write('❌ No Project Manager found')
                return
                
            user = User.objects.filter(team='TECH', is_active=True).first()
            if not user:
                self.stdout.write('❌ No Tech team user found')
                return
                
            self.stdout.write(f'👤 Using PM: {pm.name} ({pm.email})')
            self.stdout.write(f'👤 Assigning to: {user.name} ({user.email})')
            
            # Test task creation
            self.stdout.write('\n📝 Creating test task...')
            
            with transaction.atomic():
                task = Task.objects.create(
                    title='Test Task - Database Persistence',
                    description='This is a test task to verify database persistence',
                    assigned_to=user,
                    assigned_by=pm,
                    team='TECH',
                    priority='MEDIUM',
                    due_date=None
                )
                
                # Create notification
                Notification.objects.create(
                    recipient=user,
                    message=f'Test task assigned: "{task.title}" by {pm.name}'
                )
                
                self.stdout.write(f'✅ Task created with ID: {task.id}')
                self.stdout.write(f'   Title: {task.title}')
                self.stdout.write(f'   Assigned to: {task.assigned_to.name}')
                self.stdout.write(f'   Assigned by: {task.assigned_by.name}')
                self.stdout.write(f'   Status: {task.status}')
                self.stdout.write(f'   Created: {task.created_at}')
            
            # Verify task exists in database
            self.stdout.write('\n🔍 Verifying task persistence...')
            
            if Task.objects.filter(id=task.id).exists():
                saved_task = Task.objects.get(id=task.id)
                self.stdout.write('✅ Task found in database')
                self.stdout.write(f'   ID: {saved_task.id}')
                self.stdout.write(f'   Title: {saved_task.title}')
                self.stdout.write(f'   Assigned to: {saved_task.assigned_to.name}')
                self.stdout.write(f'   Status: {saved_task.status}')
            else:
                self.stdout.write('❌ Task not found in database!')
            
            # Check notification
            notification = Notification.objects.filter(
                recipient=user,
                message__icontains='Test task assigned'
            ).first()
            
            if notification:
                self.stdout.write('✅ Notification created successfully')
                self.stdout.write(f'   Message: {notification.message}')
            else:
                self.stdout.write('❌ Notification not found!')
            
            # Count total tasks
            total_tasks = Task.objects.count()
            self.stdout.write(f'\n📊 Total tasks in database: {total_tasks}')
            
            # Show all tasks
            if total_tasks > 0:
                self.stdout.write('\n📋 All tasks:')
                for t in Task.objects.all():
                    self.stdout.write(f'  - ID: {t.id}, Title: {t.title}, Status: {t.status}')
            
            self.stdout.write('\n✅ Test completed!')
            
        except Exception as e:
            self.stdout.write(f'❌ Error during test: {str(e)}')
            import traceback
            traceback.print_exc()
