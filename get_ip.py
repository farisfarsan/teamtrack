#!/usr/bin/env python
"""
Get your local IP address for team access
"""
import socket

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def main():
    """Main function"""
    ip = get_local_ip()
    print("=" * 50)
    print("TeamTrack Server Information")
    print("=" * 50)
    print(f"Local IP Address: {ip}")
    print(f"Team Access URL: http://{ip}:8000")
    print("=" * 50)
    print("\nTeam members should use the URL above to access TeamTrack")
    print("Make sure your firewall allows port 8000")
    print("=" * 50)

if __name__ == "__main__":
    main()
