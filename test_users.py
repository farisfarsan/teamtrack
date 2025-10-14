#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("=== GRYTT User Management System ===")
print()

# Get all users
users = User.objects.all().order_by('name')
print(f"Total Users: {users.count()}")
print()

if users.exists():
    print("User List:")
    print("-" * 80)
    for i, user in enumerate(users, 1):
        print(f"{i:2d}. Name: {user.name}")
        print(f"    Email: {user.email}")
        print(f"    Team: {user.get_team_display()}")
        print(f"    Active: {'Yes' if user.is_active else 'No'}")
        print(f"    Staff: {'Yes' if user.is_staff else 'No'}")
        print(f"    Superuser: {'Yes' if user.is_superuser else 'No'}")
        print()
else:
    print("No users found in the system.")

print("-" * 80)

# Check for specific user
test_email = 'kiranmoorkath@gmail.com'
if User.objects.filter(email=test_email).exists():
    user = User.objects.get(email=test_email)
    print(f"✅ User {test_email} exists!")
    print(f"   Name: {user.name}")
    print(f"   Team: {user.get_team_display()}")
    print(f"   Active: {user.is_active}")
else:
    print(f"❌ User {test_email} not found.")
