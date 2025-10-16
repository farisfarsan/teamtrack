"""
Monitoring and alerting system for TeamTrack
This system monitors service health and sends alerts when issues are detected
"""
import os
import logging
import requests
import time
import threading
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

class MonitoringSystem:
    """Comprehensive monitoring system for TeamTrack"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.check_interval = 300  # 5 minutes
        self.alert_cooldown = 1800  # 30 minutes
        self.last_alert_time = None
        self.consecutive_failures = 0
        self.max_consecutive_failures = 3
        
    def start(self):
        """Start the monitoring system"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        logger.info("Monitoring system started")
    
    def stop(self):
        """Stop the monitoring system"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Monitoring system stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                self._check_service_health()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def _check_service_health(self):
        """Check service health and send alerts if needed"""
        try:
            base_url = os.getenv('BASE_URL', 'https://teamtrack-1.onrender.com')
            
            # Check multiple endpoints
            endpoints = [
                f"{base_url}/keep-alive/",
                f"{base_url}/health/",
                f"{base_url}/",
            ]
            
            all_healthy = True
            
            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, timeout=10)
                    if response.status_code != 200:
                        all_healthy = False
                        logger.warning(f"Endpoint {endpoint} returned status {response.status_code}")
                except requests.exceptions.RequestException as e:
                    all_healthy = False
                    logger.warning(f"Endpoint {endpoint} failed: {e}")
            
            if all_healthy:
                self.consecutive_failures = 0
                logger.info("✅ All endpoints healthy")
            else:
                self.consecutive_failures += 1
                logger.warning(f"⚠️ Service health issues detected (failure #{self.consecutive_failures})")
                
                # Send alert if we have consecutive failures
                if self.consecutive_failures >= self.max_consecutive_failures:
                    self._send_alert()
                
        except Exception as e:
            logger.error(f"Health check error: {e}")
            self.consecutive_failures += 1
    
    def _send_alert(self):
        """Send alert notification"""
        try:
            # Check if we should send alert (cooldown period)
            if self.last_alert_time:
                time_since_last = timezone.now() - self.last_alert_time
                if time_since_last.total_seconds() < self.alert_cooldown:
                    logger.info("Alert cooldown active, skipping alert")
                    return
            
            logger.warning("🚨 Sending service health alert")
            
            # Send email alert
            self._send_email_alert()
            
            # Send webhook alert (if configured)
            self._send_webhook_alert()
            
            self.last_alert_time = timezone.now()
            
        except Exception as e:
            logger.error(f"Alert sending failed: {e}")
    
    def _send_email_alert(self):
        """Send email alert"""
        try:
            subject = "🚨 TeamTrack Service Health Alert"
            
            message = f"""
            Service Health Alert
            
            Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
            Service: TeamTrack
            Status: Multiple consecutive failures detected
            
            The service has experienced {self.consecutive_failures} consecutive failures.
            Please check the service status and logs.
            
            Service URL: {os.getenv('BASE_URL', 'https://teamtrack-1.onrender.com')}
            
            This is an automated alert from the TeamTrack monitoring system.
            """
            
            # Send to admin email if configured
            admin_email = os.getenv('ADMIN_EMAIL')
            if admin_email:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_email],
                    fail_silently=False,
                )
                logger.info(f"Email alert sent to {admin_email}")
            else:
                logger.info("No admin email configured, skipping email alert")
                
        except Exception as e:
            logger.error(f"Email alert failed: {e}")
    
    def _send_webhook_alert(self):
        """Send webhook alert"""
        try:
            webhook_url = os.getenv('WEBHOOK_URL')
            if not webhook_url:
                return
            
            alert_data = {
                "text": "🚨 TeamTrack Service Health Alert",
                "attachments": [
                    {
                        "color": "danger",
                        "fields": [
                            {
                                "title": "Service",
                                "value": "TeamTrack",
                                "short": True
                            },
                            {
                                "title": "Status",
                                "value": "Multiple consecutive failures",
                                "short": True
                            },
                            {
                                "title": "Failures",
                                "value": str(self.consecutive_failures),
                                "short": True
                            },
                            {
                                "title": "Time",
                                "value": timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
                                "short": True
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(webhook_url, json=alert_data, timeout=10)
            if response.status_code == 200:
                logger.info("Webhook alert sent successfully")
            else:
                logger.warning(f"Webhook alert failed with status {response.status_code}")
                
        except Exception as e:
            logger.error(f"Webhook alert failed: {e}")


class PerformanceMonitor:
    """Performance monitoring system"""
    
    def __init__(self):
        self.metrics = {}
        self.start_time = timezone.now()
    
    def record_request(self, path, method, status_code, response_time):
        """Record request metrics"""
        key = f"{method}:{path}"
        if key not in self.metrics:
            self.metrics[key] = {
                'count': 0,
                'total_time': 0,
                'status_codes': {},
                'last_request': None
            }
        
        self.metrics[key]['count'] += 1
        self.metrics[key]['total_time'] += response_time
        self.metrics[key]['last_request'] = timezone.now()
        
        status_key = str(status_code)
        if status_key not in self.metrics[key]['status_codes']:
            self.metrics[key]['status_codes'][status_key] = 0
        self.metrics[key]['status_codes'][status_key] += 1
    
    def get_metrics(self):
        """Get performance metrics"""
        uptime = timezone.now() - self.start_time
        
        return {
            'uptime_seconds': uptime.total_seconds(),
            'uptime_human': str(uptime),
            'total_requests': sum(metric['count'] for metric in self.metrics.values()),
            'endpoints': self.metrics,
            'timestamp': timezone.now().isoformat()
        }


# Global monitoring system instance
monitoring_system = MonitoringSystem()
performance_monitor = PerformanceMonitor()

def start_monitoring():
    """Start the monitoring system"""
    monitoring_system.start()

def stop_monitoring():
    """Stop the monitoring system"""
    monitoring_system.stop()

def get_performance_metrics():
    """Get performance metrics"""
    return performance_monitor.get_metrics()
