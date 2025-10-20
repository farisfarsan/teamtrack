"""
Task management utilities for recovery and maintenance
"""
from django.utils import timezone
from tasks.models import Task
import logging

logger = logging.getLogger(__name__)

class TaskManager:
    """
    Utility class for task management operations
    """
    
    @staticmethod
    def restore_all_tasks():
        """
        Restore all tasks to a default state
        Used for recovery operations
        """
        try:
            # Get all tasks
            tasks = Task.objects.all()
            restored_count = 0
            
            for task in tasks:
                # Reset task to pending if it's in an invalid state
                if task.status not in ['pending', 'in_progress', 'completed', 'cancelled']:
                    task.status = 'pending'
                    task.save()
                    restored_count += 1
            
            message = f"Restored {restored_count} tasks to valid state"
            logger.info(message)
            return True, message
            
        except Exception as e:
            error_message = f"Failed to restore tasks: {str(e)}"
            logger.error(error_message)
            return False, error_message
    
    @staticmethod
    def get_task_stats():
        """
        Get statistics about tasks
        """
        try:
            stats = {
                'total_tasks': Task.objects.count(),
                'pending_tasks': Task.objects.filter(status='pending').count(),
                'in_progress_tasks': Task.objects.filter(status='in_progress').count(),
                'completed_tasks': Task.objects.filter(status='completed').count(),
                'cancelled_tasks': Task.objects.filter(status='cancelled').count(),
            }
            return True, stats
        except Exception as e:
            return False, f"Failed to get task stats: {str(e)}"
