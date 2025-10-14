#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create user
email = 'kiranmoorkath@gmail.com'
password = 'kiran123'
name = 'Kiran Moorkath'

try:
    # Check if user already exists
    if User.objects.filter(email=email).exists():
        print(f"User {email} already exists!")
        user = User.objects.get(email=email)
        print(f"Existing user: {user.name} ({user.email})")
    else:
        # Create new user
        user = User.objects.create_user(
            email=email,
            password=password,
            name=name,
            is_active=True
        )
        print(f"User created successfully!")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        print(f"Team: {user.get_team_display()}")
        print(f"Active: {user.is_active}")
except Exception as e:
    print(f"Error creating user: {e}")
