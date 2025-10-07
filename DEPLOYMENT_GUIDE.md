# TeamTrack Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Local Network Deployment (Recommended for Teams)

#### Step 1: Prepare Your System
```bash
# Navigate to your project directory
cd C:\Users\faris\Desktop\pm_app\teamtrack

# Install dependencies
pip install -r requirements.txt

# Run deployment script
python deploy.py
```

#### Step 2: Start the Server
```bash
# Start server accessible from other computers on your network
python manage.py runserver 0.0.0.0:8000
```

#### Step 3: Find Your IP Address
```bash
# Windows
ipconfig

# Look for your local IP (usually 192.168.x.x or 10.x.x.x)
```

#### Step 4: Team Members Access
- **URL**: `http://YOUR_IP_ADDRESS:8000`
- **Example**: `http://192.168.1.100:8000`

---

### Option 2: Cloud Deployment (Heroku)

#### Step 1: Install Heroku CLI
Download from: https://devcenter.heroku.com/articles/heroku-cli

#### Step 2: Create Heroku App
```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-teamtrack-app

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set DEBUG=False
```

#### Step 3: Deploy
```bash
# Add PostgreSQL database
heroku addons:create heroku-postgresql:mini

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

---

### Option 3: VPS/Cloud Server Deployment

#### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx postgresql -y

# Create virtual environment
python3 -m venv teamtrack_env
source teamtrack_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Configure Database
```bash
# Create database
sudo -u postgres createdb teamtrack
sudo -u postgres createuser teamtrack_user
sudo -u postgres psql -c "ALTER USER teamtrack_user PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE teamtrack TO teamtrack_user;"
```

#### Step 3: Deploy Application
```bash
# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start with Gunicorn
gunicorn teamtrack.wsgi:application --bind 0.0.0.0:8000
```

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file in your project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
DB_NAME=teamtrack
DB_USER=teamtrack_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Firewall Settings
```bash
# Allow port 8000 (or your chosen port)
sudo ufw allow 8000
```

---

## 👥 Team Member Access

### Login Credentials
- **Admin**: farismullen93@gmail.com / farisgryttuser1
- **Tech Team**: 
  - dileepkrishnan92@gmail.com / dileep123
  - vyshakpk10@gmail.com / vyshak123
  - febiwilsonvazhakkan@gmail.com / febi123
- **Design Team**: muralisyam1@gmail.com / murali123

### Access Instructions for Team Members
1. Open web browser
2. Go to: `http://YOUR_SERVER_IP:8000`
3. Click "Login"
4. Enter your email and password
5. Start using TeamTrack!

---

## 🛠️ Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID_NUMBER> /F
```

#### Database Issues
```bash
# Reset database
python manage.py flush
python manage.py migrate
```

#### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput
```

---

## 🔒 Security Notes

### For Production:
1. Change `SECRET_KEY` in settings
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS` with your domain
4. Use HTTPS in production
5. Set up proper database credentials
6. Configure firewall rules

### For Local Network:
1. Ensure your firewall allows port 8000
2. Use strong passwords for all users
3. Regularly update dependencies
4. Monitor access logs

---

## 📞 Support

If you encounter any issues:
1. Check the logs in `teamtrack.log`
2. Verify all dependencies are installed
3. Ensure database is properly configured
4. Check firewall and network settings

---

## 🎯 Quick Start Commands

```bash
# Install and run locally
pip install -r requirements.txt
python deploy.py
python manage.py runserver 0.0.0.0:8000

# Access from other computers
# http://YOUR_IP:8000
```
