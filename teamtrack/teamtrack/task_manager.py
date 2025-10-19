"""
Task Management Utility for TeamTrack
Handles task creation, clearing, and error recovery with backup/restore
"""
import logging
from django.db import transaction
from django.contrib import messages
from django.core.cache import cache
from django.utils import timezone
from tasks.models import Task
from accounts.models import User
from teamtrack.task_backup_recovery import TaskBackupRecovery

logger = logging.getLogger(__name__)

class TaskManager:
    """Robust task management system with backup and recovery"""
    
    @staticmethod
    def clear_all_tasks():
        """Clear all tasks from the system"""
        try:
            with transaction.atomic():
                # Get count before deletion
                task_count = Task.objects.count()
                
                # Delete all tasks
                Task.objects.all().delete()
                
                # Clear any cached task data
                cache.delete('all_tasks')
                cache.delete('user_tasks')
                cache.delete('team_tasks')
                
                logger.info(f"Cleared {task_count} tasks from the system")
                return True, f"Cleared {task_count} tasks successfully"
                
        except Exception as e:
            logger.error(f"Failed to clear tasks: {e}")
            return False, f"Failed to clear tasks: {str(e)}"
    
    @staticmethod
    def clear_all_tasks_with_backup():
        """Clear all tasks but backup them first for recovery"""
        try:
            # First backup the tasks
            backup_success, backup_message = TaskBackupRecovery.backup_all_tasks()
            
            if not backup_success:
                logger.error(f"Backup failed: {backup_message}")
                return False, f"Backup failed: {backup_message}"
            
            # Then clear the tasks
            with transaction.atomic():
                task_count = Task.objects.count()
                Task.objects.all().delete()
                
                # Clear cached data
                cache.delete('all_tasks')
                cache.delete('user_tasks')
                cache.delete('team_tasks')
                
                logger.info(f"Cleared {task_count} tasks (backed up first)")
                return True, f"Cleared {task_count} tasks (backed up first)"
                
        except Exception as e:
            logger.error(f"Failed to clear tasks with backup: {e}")
            return False, f"Failed to clear tasks with backup: {str(e)}"
    
    @staticmethod
    def restore_all_tasks():
        """Restore all tasks from backup"""
        try:
            success, message = TaskBackupRecovery.restore_all_tasks()
            logger.info(f"Task restoration: {message}")
            return success, message
        except Exception as e:
            logger.error(f"Failed to restore tasks: {e}")
            return False, f"Failed to restore tasks: {str(e)}"
    
    @staticmethod
    def create_task_with_recovery(request, task_data):
        """Create task with automatic recovery if service goes down"""
        try:
            with transaction.atomic():
                # Attempt to create the task
                task = TaskManager._create_task(request, task_data)
                
                if task:
                    logger.info(f"Task '{task.title}' created successfully")
                    return task, "Task created successfully"
                else:
                    # If task creation failed, clear all tasks with backup
                    logger.warning("Task creation failed, clearing all tasks with backup")
                    success, message = TaskManager.clear_all_tasks_with_backup()
                    return None, f"Task creation failed. {message}"
                    
        except Exception as e:
            logger.error(f"Task creation error: {e}")
            
            # Clear all tasks with backup on any error
            logger.warning("Service error detected, clearing all tasks with backup")
            success, message = TaskManager.clear_all_tasks_with_backup()
            return None, f"Service error occurred. {message}"
    
    @staticmethod
    def _create_task(request, task_data):
        """Internal method to create a task"""
        title = task_data.get('title', '').strip()
        description = task_data.get('description', '').strip()
        assigned_to_id = task_data.get('assigned_to')
        team = task_data.get('team', 'TECH')
        priority = task_data.get('priority', 'MEDIUM')
        due_date = task_data.get('due_date')
        
        # Validate required fields
        if not title:
            raise ValueError('Task title is required')
        if not assigned_to_id:
            raise ValueError('Please select a user to assign the task to')
        
        # Get assigned user
        try:
            assigned_to = User.objects.get(id=assigned_to_id, is_active=True)
        except User.DoesNotExist:
            raise ValueError('Selected user not found or inactive')
        
        # Create the task
        task = Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_to,
            assigned_by=request.user,
            team=team,
            priority=priority,
            due_date=due_date if due_date else None
        )
        
        # Clear cached data
        cache.delete('all_tasks')
        cache.delete(f'user_tasks_{assigned_to.id}')
        cache.delete(f'team_tasks_{team}')
        
        return task
    
    @staticmethod
    def handle_service_downtime():
        """Handle service downtime by clearing all tasks with backup"""
        logger.warning("Service downtime detected, clearing all tasks with backup")
        success, message = TaskManager.clear_all_tasks_with_backup()
        
        if success:
            logger.info("Tasks cleared with backup successfully due to service downtime")
        else:
            logger.error(f"Failed to clear tasks during downtime: {message}")
        
        return success, message
    
    @staticmethod
    def handle_service_recovery():
        """Handle service recovery by attempting to restore tasks"""
        logger.info("Service recovery detected, attempting to restore tasks")
        success, message = TaskManager.restore_all_tasks()
        
        if success:
            logger.info("Tasks restored successfully after service recovery")
        else:
            logger.info(f"No tasks to restore or restoration failed: {message}")
        
        return success, message
    
    @staticmethod
    def get_backup_info():
        """Get information about current backup"""
        return TaskBackupRecovery.get_backup_info()
    
    @staticmethod
    def get_task_statistics():
        """Get task statistics"""
        try:
            total_tasks = Task.objects.count()
            completed_tasks = Task.objects.filter(status='COMPLETED').count()
            pending_tasks = Task.objects.filter(status='PENDING').count()
            in_progress_tasks = Task.objects.filter(status='IN_PROGRESS').count()
            
            completion_rate = round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
            
            return {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'in_progress_tasks': in_progress_tasks,
                'completion_rate': completion_rate
            }
        except Exception as e:
            logger.error(f"Failed to get task statistics: {e}")
            return {
                'total_tasks': 0,
                'completed_tasks': 0,
                'pending_tasks': 0,
                'in_progress_tasks': 0,
                'completion_rate': 0
            }
