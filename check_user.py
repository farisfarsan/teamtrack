#!/usr/bin/env python
import os
import sys
import django

# Add the teamtrack directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'teamtrack'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamtrack.settings')
django.setup()

from accounts.models import User

print("Users in database:")
users = User.objects.all()
if users:
    for user in users:
        print(f"Email: {user.email}, Name: {user.name}, Active: {user.is_active}")
else:
    print("No users found in database")

# Check specifically for kiranmoorkath@gmail.com
try:
    kiran_user = User.objects.get(email='kiranmoorkath@gmail.com')
    print(f"\nFound user: {kiran_user.email}")
    print(f"Name: {kiran_user.name}")
    print(f"Active: {kiran_user.is_active}")
    print(f"Staff: {kiran_user.is_staff}")
    print(f"Team: {kiran_user.team}")
except User.DoesNotExist:
    print("\nUser kiranmoorkath@gmail.com not found in database")
