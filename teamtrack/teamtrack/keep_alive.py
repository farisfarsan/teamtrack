from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import requests
import threading
import time
import os

@csrf_exempt
@require_http_methods(["GET", "POST"])
def keep_alive_ping(request):
    """Keep-alive endpoint to prevent Render from sleeping"""
    return JsonResponse({
        'status': 'alive',
        'timestamp': timezone.now().isoformat(),
        'message': 'GRYTT is running and ready!'
    })

def ping_self():
    """Function to ping the application itself"""
    try:
        # Get the current application URL
        base_url = os.getenv('BASE_URL', 'https://teamtrack-1.onrender.com')
        ping_url = f"{base_url}/keep-alive/"
        
        # Ping the application
        response = requests.get(ping_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Keep-alive ping successful at {timezone.now()}")
        else:
            print(f"⚠️ Keep-alive ping failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Keep-alive ping error: {e}")

def start_keep_alive():
    """Start the keep-alive thread"""
    def keep_alive_loop():
        while True:
            try:
                ping_self()
                # Ping every 10 minutes (600 seconds)
                time.sleep(600)
            except Exception as e:
                print(f"Keep-alive loop error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    # Start the keep-alive thread
    thread = threading.Thread(target=keep_alive_loop, daemon=True)
    thread.start()
    print("🚀 Keep-alive system started")

# Start keep-alive when module is imported
start_keep_alive()
