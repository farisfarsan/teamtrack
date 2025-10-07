#!/usr/bin/env python
"""
Vercel Deployment Helper Script
"""
import os
import subprocess
import sys

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

# Vercel
.vercel/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✅ .gitignore created")

def add_and_commit():
    """Add all files and commit"""
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit for Vercel deployment'], check=True)
        print("✅ Files committed to git")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing files: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 Vercel Deployment Helper")
    print("=" * 40)
    
    # Check git
    if not check_git():
        return
    
    # Initialize git
    init_git()
    
    # Create .gitignore
    create_gitignore()
    
    # Add and commit files
    if add_and_commit():
        print("\n🎉 Ready for Vercel deployment!")
        print("\nNext steps:")
        print("1. Create a GitHub account at https://github.com")
        print("2. Create a new repository called 'teamtrack'")
        print("3. Run these commands:")
        print("   git remote add origin https://github.com/YOUR_USERNAME/teamtrack.git")
        print("   git branch -M main")
        print("   git push -u origin main")
        print("4. Go to https://vercel.com and sign up with GitHub")
        print("5. Click 'New Project' and import your repository")
        print("6. Configure environment variables:")
        print("   - SECRET_KEY: your-secret-key-here")
        print("   - DEBUG: False")
        print("   - ALLOWED_HOSTS: your-domain.vercel.app")
        print("7. Add PostgreSQL database (Vercel Postgres)")
        print("8. Deploy!")
        print("\nYour team will be able to access TeamTrack from anywhere!")
    else:
        print("\n❌ Deployment preparation failed")

if __name__ == '__main__':
    main()
