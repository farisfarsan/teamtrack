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

print("=== FAKE USERS CHECK ===")
fake_users = User.objects.filter(email__endswith='@example.com')
print(f'Fake users currently in database: {fake_users.count()}')
for user in fake_users:
    print(f'- {user.email} ({user.name})')

print("\n=== ALL USERS ===")
all_users = User.objects.all()
print(f'Total users: {all_users.count()}')
for user in all_users:
    print(f'- {user.email} ({user.name}) - Team: {user.get_team_display()}')
