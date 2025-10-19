#!/usr/bin/env python3
"""
Database Backup Script for Render
This script creates backups of your PostgreSQL database
"""

import os
import subprocess
import datetime
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create database backup'

    def handle(self, *args, **options):
        """Create a database backup"""
        
        # Get database URL from environment
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            self.stdout.write(
                self.style.ERROR('DATABASE_URL not found in environment')
            )
            return
        
        # Create backup filename with timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'backup_{timestamp}.sql'
        
        try:
            # Create backup using pg_dump
            cmd = f'pg_dump "{database_url}" > {backup_filename}'
            subprocess.run(cmd, shell=True, check=True)
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Backup created: {backup_filename}')
            )
            
            # Get file size
            file_size = os.path.getsize(backup_filename)
            self.stdout.write(f'📁 Backup size: {file_size / 1024:.2f} KB')
            
        except subprocess.CalledProcessError as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Backup failed: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'💥 Unexpected error: {e}')
            )
