"""
Startup Recovery System for TeamTrack
Automatically attempts to restore tasks when service starts up
"""
import logging
import threading
import time
from django.utils import timezone
from teamtrack.task_backup_recovery import TaskBackupRecovery
from teamtrack.task_manager import TaskManager

logger = logging.getLogger(__name__)

class StartupRecoverySystem:
    """System to handle startup recovery"""
    
    def __init__(self):
        self.recovery_attempted = False
        self.recovery_thread = None
    
    def start_recovery(self):
        """Start the recovery process"""
        if self.recovery_attempted:
            return
        
        self.recovery_attempted = True
        
        # Start recovery in a separate thread to avoid blocking startup
        self.recovery_thread = threading.Thread(target=self._perform_recovery, daemon=True)
        self.recovery_thread.start()
        logger.info("Startup recovery system started")
    
    def _perform_recovery(self):
        """Perform the actual recovery"""
        try:
            # Wait a bit for the service to fully start
            time.sleep(10)
            
            logger.info("Performing startup recovery...")
            
            # Attempt auto-recovery
            success, message = TaskBackupRecovery.auto_recovery_on_startup()
            
            if success:
                logger.info(f"✅ Startup recovery successful: {message}")
            else:
                logger.info(f"ℹ️ Startup recovery: {message}")
                
        except Exception as e:
            logger.error(f"Startup recovery error: {e}")
    
    def get_recovery_status(self):
        """Get recovery status"""
        return {
            'recovery_attempted': self.recovery_attempted,
            'backup_info': TaskBackupRecovery.get_backup_info()
        }


# Global recovery system instance
startup_recovery = StartupRecoverySystem()

def start_recovery_on_startup():
    """Start recovery process on startup"""
    startup_recovery.start_recovery()

def get_recovery_status():
    """Get current recovery status"""
    return startup_recovery.get_recovery_status()
