#!/bin/bash
# Keep-Alive Script for Render.com
# This script runs every 10 minutes to ping your Render app

# Your Render app URL - UPDATE THIS WITH YOUR ACTUAL URL
RENDER_URL="https://your-app-name.onrender.com"

# Function to ping the app
ping_app() {
    echo "$(date): Pinging Render app..."
    
    # Try to ping the health endpoint
    response=$(curl -s -o /dev/null -w "%{http_code}" "$RENDER_URL/health/" --max-time 30)
    
    if [ "$response" = "200" ]; then
        echo "$(date): ✅ App pinged successfully - Status: $response"
    else
        echo "$(date): ⚠️ App responded with status: $response"
    fi
}

# Main loop
echo "$(date): 🚀 Starting keep-alive service for Render app"
echo "$(date): 📡 Target URL: $RENDER_URL"

while true; do
    ping_app
    echo "$(date): ⏰ Waiting 10 minutes before next ping..."
    sleep 600  # 10 minutes
done
