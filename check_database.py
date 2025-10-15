#!/usr/bin/env python
import os
import sys
import django

# Add the teamtrack directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'teamtrack'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamtrack.settings')
django.setup()

from django.db import connection
from tasks.models import Task, TaskComment
from accounts.models import User

print("=== DATABASE ANALYSIS ===")

# Check database tables
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"\nDatabase tables ({len(tables)}):")
for table in tables:
    print(f"- {table[0]}")

# Check task data
print(f"\n=== TASK DATA ===")
print(f"Total tasks: {Task.objects.count()}")
print(f"Total comments: {TaskComment.objects.count()}")
print(f"Total users: {User.objects.count()}")

# Show recent tasks if any exist
tasks = Task.objects.all().order_by('-created_at')[:5]
if tasks:
    print(f"\nRecent tasks:")
    for task in tasks:
        print(f"- {task.title} (Created: {task.created_at}, Status: {task.status})")
else:
    print("\nNo tasks found in database")

# Check if there are any task-related tables with data
cursor.execute("SELECT COUNT(*) FROM tasks_task")
task_count = cursor.fetchone()[0]
print(f"\nDirect SQL query - tasks_task table: {task_count} rows")

cursor.execute("SELECT COUNT(*) FROM tasks_taskcomment")
comment_count = cursor.fetchone()[0]
print(f"Direct SQL query - tasks_taskcomment table: {comment_count} rows")
