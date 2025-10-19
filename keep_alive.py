#!/usr/bin/env python3
"""
Keep-Alive Script for Render.com
This script pings your Render app every 10 minutes to prevent sleep mode
"""

import requests
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Your Render app URL
RENDER_APP_URL = "https://your-app-name.onrender.com"

def ping_app():
    """Ping the Render app to keep it alive"""
    try:
        response = requests.get(f"{RENDER_APP_URL}/health/", timeout=30)
        if response.status_code == 200:
            logger.info(f"✅ App pinged successfully - Status: {response.status_code}")
            return True
        else:
            logger.warning(f"⚠️ App responded with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to ping app: {e}")
        return False

def main():
    """Main keep-alive loop"""
    logger.info("🚀 Starting keep-alive service for Render app")
    logger.info(f"📡 Target URL: {RENDER_APP_URL}")
    
    while True:
        try:
            ping_app()
            # Wait 10 minutes before next ping
            logger.info("⏰ Waiting 10 minutes before next ping...")
            time.sleep(600)  # 10 minutes
        except KeyboardInterrupt:
            logger.info("🛑 Keep-alive service stopped by user")
            break
        except Exception as e:
            logger.error(f"💥 Unexpected error: {e}")
            time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    main()
