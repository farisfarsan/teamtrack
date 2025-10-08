#!/usr/bin/env python3
"""
External Keep-Alive Script for GRYTT Application
Run this script to keep your GRYTT app alive 24/7

Usage:
    python keep_alive_external.py

Or set up as a cron job to run every 10 minutes:
    */10 * * * * /usr/bin/python3 /path/to/keep_alive_external.py
"""

import requests
import time
import datetime
import sys

# Configuration
APP_URL = "https://teamtrack-1.onrender.com"
KEEP_ALIVE_ENDPOINT = f"{APP_URL}/keep-alive/"
HEALTH_ENDPOINT = f"{APP_URL}/health/"
PING_INTERVAL = 600  # 10 minutes in seconds

def ping_app():
    """Ping the application to keep it alive"""
    try:
        print(f"[{datetime.datetime.now()}] Pinging GRYTT application...")
        
        # Ping the keep-alive endpoint
        response = requests.get(KEEP_ALIVE_ENDPOINT, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Keep-alive successful: {data.get('message', 'OK')}")
            return True
        else:
            print(f"⚠️ Keep-alive failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - app might be starting up")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - app might be sleeping")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_health():
    """Check application health"""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"🏥 Health check: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"⚠️ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def main():
    """Main keep-alive loop"""
    print("🚀 GRYTT Keep-Alive Service Started")
    print(f"📡 Monitoring: {APP_URL}")
    print(f"⏰ Ping interval: {PING_INTERVAL} seconds")
    print("=" * 50)
    
    consecutive_failures = 0
    max_failures = 3
    
    while True:
        try:
            # Ping the application
            success = ping_app()
            
            if success:
                consecutive_failures = 0
                # Also check health occasionally
                if datetime.datetime.now().minute % 30 == 0:  # Every 30 minutes
                    check_health()
            else:
                consecutive_failures += 1
                print(f"⚠️ Consecutive failures: {consecutive_failures}/{max_failures}")
                
                if consecutive_failures >= max_failures:
                    print("🚨 Too many failures - app might be down")
                    # Try to wake up the app by pinging multiple times
                    for i in range(5):
                        print(f"🔄 Attempting to wake up app (attempt {i+1}/5)...")
                        if ping_app():
                            print("✅ App is back online!")
                            consecutive_failures = 0
                            break
                        time.sleep(30)  # Wait 30 seconds between attempts
            
            # Wait for the next ping
            print(f"⏳ Next ping in {PING_INTERVAL} seconds...")
            time.sleep(PING_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n👋 Keep-alive service stopped by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    main()
