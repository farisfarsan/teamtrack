"""
Automated recovery system for TeamTrack
This system automatically detects and recovers from common issues
"""
import os
import logging
import time
import threading
from django.core.management import call_command
from django.core.cache import cache
from django.db import connection
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

class AutoRecoverySystem:
    """Automated recovery system for common issues"""
    
    def __init__(self):
        self.recovery_enabled = True
        self.last_recovery_time = None
        self.recovery_count = 0
        self.max_recoveries_per_hour = 5
        
    def check_and_recover_database(self):
        """Check database connectivity and recover if needed"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result[0] != 1:
                    logger.warning("Database query failed, attempting recovery")
                    self._recover_database()
                    return False
            return True
        except Exception as e:
            logger.error(f"Database check failed: {e}")
            self._recover_database()
            return False
    
    def _recover_database(self):
        """Attempt to recover database connection"""
        try:
            logger.info("Attempting database recovery...")
            
            # Close existing connections
            connection.close()
            
            # Wait a moment
            time.sleep(2)
            
            # Test new connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result[0] == 1:
                    logger.info("Database recovery successful")
                    self._log_recovery("database")
                    return True
            
            logger.error("Database recovery failed")
            return False
            
        except Exception as e:
            logger.error(f"Database recovery error: {e}")
            return False
    
    def check_and_recover_cache(self):
        """Check cache system and recover if needed"""
        try:
            test_key = f"recovery_test_{int(time.time())}"
            test_value = "test_value"
            
            # Test cache
            cache.set(test_key, test_value, 30)
            retrieved_value = cache.get(test_key)
            
            if retrieved_value != test_value:
                logger.warning("Cache system failed, attempting recovery")
                self._recover_cache()
                return False
            
            cache.delete(test_key)
            return True
            
        except Exception as e:
            logger.error(f"Cache check failed: {e}")
            self._recover_cache()
            return False
    
    def _recover_cache(self):
        """Attempt to recover cache system"""
        try:
            logger.info("Attempting cache recovery...")
            
            # Clear cache
            cache.clear()
            
            # Wait a moment
            time.sleep(1)
            
            # Test cache
            test_key = f"recovery_test_{int(time.time())}"
            test_value = "test_value"
            
            cache.set(test_key, test_value, 30)
            retrieved_value = cache.get(test_key)
            
            if retrieved_value == test_value:
                logger.info("Cache recovery successful")
                self._log_recovery("cache")
                cache.delete(test_key)
                return True
            
            logger.error("Cache recovery failed")
            return False
            
        except Exception as e:
            logger.error(f"Cache recovery error: {e}")
            return False
    
    def check_and_recover_static_files(self):
        """Check static files and recover if needed"""
        try:
            static_root = settings.STATIC_ROOT
            
            if not os.path.exists(static_root):
                logger.warning("Static files directory missing, attempting recovery")
                self._recover_static_files()
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Static files check failed: {e}")
            self._recover_static_files()
            return False
    
    def _recover_static_files(self):
        """Attempt to recover static files"""
        try:
            logger.info("Attempting static files recovery...")
            
            # Run collectstatic command
            call_command('collectstatic', '--noinput', verbosity=0)
            
            logger.info("Static files recovery successful")
            self._log_recovery("static_files")
            return True
            
        except Exception as e:
            logger.error(f"Static files recovery error: {e}")
            return False
    
    def _log_recovery(self, recovery_type):
        """Log recovery attempt"""
        self.last_recovery_time = timezone.now()
        self.recovery_count += 1
        
        logger.info(f"Recovery successful: {recovery_type} (attempt #{self.recovery_count})")
    
    def can_attempt_recovery(self):
        """Check if recovery can be attempted"""
        if not self.recovery_enabled:
            return False
        
        if self.last_recovery_time is None:
            return True
        
        # Check if we've exceeded max recoveries per hour
        time_since_last = timezone.now() - self.last_recovery_time
        if time_since_last.total_seconds() < 3600:  # Less than 1 hour
            if self.recovery_count >= self.max_recoveries_per_hour:
                logger.warning("Maximum recovery attempts per hour exceeded")
                return False
        
        return True
    
    def run_recovery_checks(self):
        """Run all recovery checks"""
        if not self.can_attempt_recovery():
            return
        
        logger.info("Running automated recovery checks...")
        
        # Check and recover database
        if not self.check_and_recover_database():
            logger.warning("Database recovery failed")
        
        # Check and recover cache
        if not self.check_and_recover_cache():
            logger.warning("Cache recovery failed")
        
        # Check and recover static files
        if not self.check_and_recover_static_files():
            logger.warning("Static files recovery failed")
        
        logger.info("Automated recovery checks completed")


class RecoveryScheduler:
    """Scheduler for automated recovery checks"""
    
    def __init__(self):
        self.recovery_system = AutoRecoverySystem()
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the recovery scheduler"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        logger.info("Recovery scheduler started")
    
    def stop(self):
        """Stop the recovery scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Recovery scheduler stopped")
    
    def _run_scheduler(self):
        """Main scheduler loop"""
        while self.running:
            try:
                # Run recovery checks every 5 minutes
                self.recovery_system.run_recovery_checks()
                time.sleep(300)  # 5 minutes
            except Exception as e:
                logger.error(f"Recovery scheduler error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying


# Global recovery scheduler instance
recovery_scheduler = RecoveryScheduler()

def start_auto_recovery():
    """Start the automated recovery system"""
    recovery_scheduler.start()

def stop_auto_recovery():
    """Stop the automated recovery system"""
    recovery_scheduler.stop()
