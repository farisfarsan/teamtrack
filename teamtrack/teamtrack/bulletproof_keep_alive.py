"""
Bulletproof keep-alive system for TeamTrack
This system ensures the service stays alive with minimal dependencies
"""
import os
import requests
import threading
import time
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

class BulletproofKeepAlive:
    """Bulletproof keep-alive system"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.base_url = os.getenv('BASE_URL', 'https://teamtrack-1.onrender.com')
        self.ping_interval = 300  # 5 minutes
        
    def start(self):
        """Start the keep-alive system"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._ping_loop, daemon=True)
        self.thread.start()
        logger.info("Bulletproof keep-alive system started")
    
    def stop(self):
        """Stop the keep-alive system"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Bulletproof keep-alive system stopped")
    
    def _ping_loop(self):
        """Main ping loop"""
        while self.running:
            try:
                self._ping_service()
                time.sleep(self.ping_interval)
            except Exception as e:
                logger.error(f"Keep-alive ping error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def _ping_service(self):
        """Ping the service"""
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


# Global keep-alive instance
bulletproof_keep_alive = BulletproofKeepAlive()

def start_bulletproof_keep_alive():
    """Start the bulletproof keep-alive system"""
    bulletproof_keep_alive.start()

def stop_bulletproof_keep_alive():
    """Stop the bulletproof keep-alive system"""
    bulletproof_keep_alive.stop()

# Start keep-alive when module is imported
start_bulletproof_keep_alive()
