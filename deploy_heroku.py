#!/usr/bin/env python
"""
Heroku Deployment Helper Script
"""
import os
import subprocess
import sys

def check_heroku_cli():
    """Check if Heroku CLI is installed"""
    try:
        result = subprocess.run(['heroku', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Heroku CLI is installed")
            return True
        else:
            print("❌ Heroku CLI is not installed")
            return False
    except FileNotFoundError:
        print("❌ Heroku CLI is not installed. Please install from https://devcenter.heroku.com/articles/heroku-cli")
        return False

def check_git():
    """Check if git is installed and initialized"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git is installed")
            return True
        else:
            print("❌ Git is not installed")
            return False
    except FileNotFoundError:
        print("❌ Git is not installed. Please install Git from https://git-scm.com")
        return False

def init_git():
    """Initialize git repository if not already done"""
    if not os.path.exists('.git'):
        print("Initializing git repository...")
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git repository initialized")
    else:
        print("✅ Git repository already exists")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Django
*.pyc
__pycache__/
*.log
db.sqlite3
media/
staticfiles/

# Environment variables
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Heroku
.heroku/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✅ .gitignore created")

def add_and_commit():
    """Add all files and commit"""
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit for Heroku deployment'], check=True)
        print("✅ Files committed to git")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing files: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 Heroku Deployment Helper")
    print("=" * 40)
    
    # Check requirements
    if not check_heroku_cli() or not check_git():
        return
    
    # Initialize git
    init_git()
    
    # Create .gitignore
    create_gitignore()
    
    # Add and commit files
    if add_and_commit():
        print("\n🎉 Ready for Heroku deployment!")
        print("\nNext steps:")
        print("1. Login to Heroku:")
        print("   heroku login")
        print("2. Create Heroku app:")
        print("   heroku create your-teamtrack-app")
        print("3. Add PostgreSQL database:")
        print("   heroku addons:create heroku-postgresql:mini")
        print("4. Set environment variables:")
        print("   heroku config:set SECRET_KEY=your-secret-key-here")
        print("   heroku config:set DEBUG=False")
        print("5. Deploy:")
        print("   git push heroku main")
        print("6. Run migrations:")
        print("   heroku run python manage.py migrate")
        print("\nYour team will be able to access TeamTrack from anywhere!")
    else:
        print("\n❌ Deployment preparation failed")

if __name__ == '__main__':
    main()
