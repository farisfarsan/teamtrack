"""
Enhanced keep-alive system with multiple strategies
This prevents Render from sleeping and maintains service availability
"""
import os
import requests
import threading
import time
import logging
from django.utils import timezone
from django.conf import settings
from .auto_recovery import start_auto_recovery

logger = logging.getLogger(__name__)

class KeepAliveManager:
    """Enhanced keep-alive manager with multiple strategies"""
    
    def __init__(self):
        self.running = False
        self.threads = []
        self.base_url = os.getenv('BASE_URL', 'https://teamtrack-1.onrender.com')
        self.ping_interval = 300  # 5 minutes
        self.health_check_interval = 600  # 10 minutes
        self.recovery_check_interval = 900  # 15 minutes
        
    def start(self):
        """Start all keep-alive strategies"""
        if self.running:
            return
        
        self.running = True
        logger.info("Starting enhanced keep-alive system...")
        
        # Start multiple keep-alive strategies
        self._start_ping_strategy()
        self._start_health_check_strategy()
        self._start_recovery_strategy()
        
        # Start auto-recovery system
        start_auto_recovery()
        
        logger.info("Enhanced keep-alive system started successfully")
    
    def stop(self):
        """Stop all keep-alive strategies"""
        self.running = False
        
        # Wait for threads to finish
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=5)
        
        self.threads.clear()
        logger.info("Enhanced keep-alive system stopped")
    
    def _start_ping_strategy(self):
        """Start ping strategy - basic keep-alive"""
        def ping_loop():
            while self.running:
                try:
                    self._ping_endpoint()
                    time.sleep(self.ping_interval)
                except Exception as e:
                    logger.error(f"Ping strategy error: {e}")
                    time.sleep(60)  # Wait 1 minute before retrying
        
        thread = threading.Thread(target=ping_loop, daemon=True)
        thread.start()
        self.threads.append(thread)
        logger.info("Ping strategy started")
    
    def _start_health_check_strategy(self):
        """Start health check strategy - comprehensive monitoring"""
        def health_check_loop():
            while self.running:
                try:
                    self._health_check_endpoint()
                    time.sleep(self.health_check_interval)
                except Exception as e:
                    logger.error(f"Health check strategy error: {e}")
                    time.sleep(120)  # Wait 2 minutes before retrying
        
        thread = threading.Thread(target=health_check_loop, daemon=True)
        thread.start()
        self.threads.append(thread)
        logger.info("Health check strategy started")
    
    def _start_recovery_strategy(self):
        """Start recovery strategy - automated recovery"""
        def recovery_loop():
            while self.running:
                try:
                    self._recovery_check()
                    time.sleep(self.recovery_check_interval)
                except Exception as e:
                    logger.error(f"Recovery strategy error: {e}")
                    time.sleep(180)  # Wait 3 minutes before retrying
        
        thread = threading.Thread(target=recovery_loop, daemon=True)
        thread.start()
        self.threads.append(thread)
        logger.info("Recovery strategy started")
    
    def _ping_endpoint(self):
        """Ping the keep-alive endpoint"""
        try:
            ping_url = f"{self.base_url}/keep-alive/"
            response = requests.get(ping_url, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"✅ Keep-alive ping successful at {timezone.now()}")
            else:
                logger.warning(f"⚠️ Keep-alive ping failed with status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Keep-alive ping error: {e}")
        except Exception as e:
            logger.error(f"❌ Unexpected ping error: {e}")
    
    def _health_check_endpoint(self):
        """Check the health endpoint"""
        try:
            health_url = f"{self.base_url}/health/"
            response = requests.get(health_url, timeout=15)
            
            if response.status_code == 200:
                health_data = response.json()
                overall_status = health_data.get('overall_status', 'unknown')
                logger.info(f"✅ Health check successful - Status: {overall_status}")
                
                # Log any warnings or issues
                if overall_status in ['warning', 'unhealthy', 'critical']:
                    logger.warning(f"⚠️ Health check detected issues: {overall_status}")
                    
            else:
                logger.warning(f"⚠️ Health check failed with status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Health check error: {e}")
        except Exception as e:
            logger.error(f"❌ Unexpected health check error: {e}")
    
    def _recovery_check(self):
        """Perform recovery check"""
        try:
            # Check if service is responding
            ping_url = f"{self.base_url}/keep-alive/"
            response = requests.get(ping_url, timeout=10)
            
            if response.status_code != 200:
                logger.warning("Service not responding properly, triggering recovery")
                self._trigger_recovery()
            else:
                logger.info("✅ Recovery check passed - service is healthy")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Recovery check error: {e}")
            self._trigger_recovery()
        except Exception as e:
            logger.error(f"❌ Unexpected recovery check error: {e}")
    
    def _trigger_recovery(self):
        """Trigger recovery procedures"""
        try:
            logger.info("🔄 Triggering recovery procedures...")
            
            # Try to ping multiple endpoints
            endpoints = [
                f"{self.base_url}/keep-alive/",
                f"{self.base_url}/health/",
                f"{self.base_url}/",
            ]
            
            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, timeout=5)
                    if response.status_code == 200:
                        logger.info(f"✅ Recovery successful via {endpoint}")
                        return
                except:
                    continue
            
            logger.error("❌ All recovery attempts failed")
            
        except Exception as e:
            logger.error(f"❌ Recovery trigger error: {e}")


# Global keep-alive manager instance
keep_alive_manager = KeepAliveManager()

def start_enhanced_keep_alive():
    """Start the enhanced keep-alive system"""
    keep_alive_manager.start()

def stop_enhanced_keep_alive():
    """Stop the enhanced keep-alive system"""
    keep_alive_manager.stop()

# Start keep-alive when module is imported
start_enhanced_keep_alive()
