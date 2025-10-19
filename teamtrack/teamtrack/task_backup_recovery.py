"""
Task Backup and Recovery System for TeamTrack
Backs up tasks before clearing and restores them when service recovers
"""
import json
import logging
import os
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone
from tasks.models import Task
from accounts.models import User

logger = logging.getLogger(__name__)

class TaskBackupRecovery:
    """Task backup and recovery system"""
    
    BACKUP_KEY = 'task_backup_data'
    BACKUP_TIMESTAMP_KEY = 'task_backup_timestamp'
    
    @staticmethod
    def backup_all_tasks():
        """Backup all tasks to cache before clearing"""
        try:
            with transaction.atomic():
                # Get all tasks with their data
                tasks_data = []
                for task in Task.objects.all():
                    task_data = {
                        'id': task.id,
                        'title': task.title,
                        'description': task.description,
                        'assigned_to_id': task.assigned_to.id,
                        'assigned_by_id': task.assigned_by.id if task.assigned_by else None,
                        'team': task.team,
                        'status': task.status,
                        'priority': task.priority,
                        'due_date': task.due_date.isoformat() if task.due_date else None,
                        'created_at': task.created_at.isoformat(),
                        'updated_at': task.updated_at.isoformat(),
                    }
                    tasks_data.append(task_data)
                
                # Store backup in cache
                cache.set(TaskBackupRecovery.BACKUP_KEY, json.dumps(tasks_data), 86400)  # 24 hours
                cache.set(TaskBackupRecovery.BACKUP_TIMESTAMP_KEY, timezone.now().isoformat(), 86400)
                
                logger.info(f"Backed up {len(tasks_data)} tasks successfully")
                return True, f"Backed up {len(tasks_data)} tasks"
                
        except Exception as e:
            logger.error(f"Failed to backup tasks: {e}")
            return False, f"Failed to backup tasks: {str(e)}"
    
    @staticmethod
    def restore_all_tasks():
        """Restore all tasks from backup"""
        try:
            # Check if backup exists
            backup_data = cache.get(TaskBackupRecovery.BACKUP_KEY)
            if not backup_data:
                logger.warning("No backup data found to restore")
                return False, "No backup data found to restore"
            
            # Parse backup data
            tasks_data = json.loads(backup_data)
            
            with transaction.atomic():
                restored_count = 0
                failed_count = 0
                
                for task_data in tasks_data:
                    try:
                        # Get assigned user
                        assigned_to = User.objects.get(id=task_data['assigned_to_id'])
                        
                        # Get assigned by user (if exists)
                        assigned_by = None
                        if task_data['assigned_by_id']:
                            try:
                                assigned_by = User.objects.get(id=task_data['assigned_by_id'])
                            except User.DoesNotExist:
                                logger.warning(f"Assigned by user {task_data['assigned_by_id']} not found")
                        
                        # Create task
                        task = Task.objects.create(
                            title=task_data['title'],
                            description=task_data['description'],
                            assigned_to=assigned_to,
                            assigned_by=assigned_by,
                            team=task_data['team'],
                            status=task_data['status'],
                            priority=task_data['priority'],
                            due_date=task_data['due_date'] if task_data['due_date'] else None,
                        )
                        
                        restored_count += 1
                        logger.info(f"Restored task: {task.title}")
                        
                    except Exception as e:
                        failed_count += 1
                        logger.error(f"Failed to restore task {task_data.get('title', 'Unknown')}: {e}")
                
                # Clear backup after successful restoration
                if restored_count > 0:
                    cache.delete(TaskBackupRecovery.BACKUP_KEY)
                    cache.delete(TaskBackupRecovery.BACKUP_TIMESTAMP_KEY)
                
                logger.info(f"Restored {restored_count} tasks, {failed_count} failed")
                return True, f"Restored {restored_count} tasks, {failed_count} failed"
                
        except Exception as e:
            logger.error(f"Failed to restore tasks: {e}")
            return False, f"Failed to restore tasks: {str(e)}"
    
    @staticmethod
    def clear_all_tasks_with_backup():
        """Clear all tasks but backup them first"""
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
    def get_backup_info():
        """Get information about current backup"""
        try:
            backup_data = cache.get(TaskBackupRecovery.BACKUP_KEY)
            backup_timestamp = cache.get(TaskBackupRecovery.BACKUP_TIMESTAMP_KEY)
            
            if backup_data:
                tasks_data = json.loads(backup_data)
                return {
                    'has_backup': True,
                    'task_count': len(tasks_data),
                    'backup_timestamp': backup_timestamp,
                    'backup_age': timezone.now() - timezone.datetime.fromisoformat(backup_timestamp) if backup_timestamp else None
                }
            else:
                return {
                    'has_backup': False,
                    'task_count': 0,
                    'backup_timestamp': None,
                    'backup_age': None
                }
                
        except Exception as e:
            logger.error(f"Failed to get backup info: {e}")
            return {
                'has_backup': False,
                'task_count': 0,
                'backup_timestamp': None,
                'backup_age': None,
                'error': str(e)
            }
    
    @staticmethod
    def auto_recovery_on_startup():
        """Automatically attempt recovery on service startup"""
        try:
            backup_info = TaskBackupRecovery.get_backup_info()
            
            if backup_info['has_backup']:
                logger.info(f"Found backup with {backup_info['task_count']} tasks, attempting recovery...")
                
                # Check if backup is not too old (less than 24 hours)
                if backup_info['backup_age'] and backup_info['backup_age'].total_seconds() < 86400:
                    success, message = TaskBackupRecovery.restore_all_tasks()
                    
                    if success:
                        logger.info(f"Auto-recovery successful: {message}")
                        return True, f"Auto-recovery successful: {message}"
                    else:
                        logger.error(f"Auto-recovery failed: {message}")
                        return False, f"Auto-recovery failed: {message}"
                else:
                    logger.warning("Backup is too old, skipping auto-recovery")
                    return False, "Backup is too old, skipping auto-recovery"
            else:
                logger.info("No backup found, skipping auto-recovery")
                return False, "No backup found, skipping auto-recovery"
                
        except Exception as e:
            logger.error(f"Auto-recovery error: {e}")
            return False, f"Auto-recovery error: {str(e)}"
