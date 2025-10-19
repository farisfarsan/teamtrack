# 🚀 Render Deployment with Keep-Alive - Complete Guide

## 📋 Quick Setup (5 Minutes)

### Step 1: Deploy to Render
1. **Go to [render.com](https://render.com)** and sign up
2. **Connect your GitHub** repository
3. **Create Web Service**:
   - **Name**: `teamtrack`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn teamtrack.wsgi:application --settings=teamtrack.settings_render`

### Step 2: Add PostgreSQL Database
1. **Create Database** in Render dashboard
2. **Copy the Database URL**
3. **Add Environment Variables**:
   ```
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   DATABASE_URL=postgresql://user:pass@host:port/db
   ```

### Step 3: Set Up Keep-Alive (Choose One)

#### Option A: UptimeRobot (Recommended - FREE)
1. **Go to [uptimerobot.com](https://uptimerobot.com)**
2. **Sign up for free**
3. **Add Monitor**:
   - **Type**: HTTP(s)
   - **URL**: `https://your-app-name.onrender.com/health/`
   - **Interval**: 5 minutes
   - **Timeout**: 30 seconds

#### Option B: GitHub Actions (FREE)
Create `.github/workflows/keep-alive.yml`:
```yaml
name: Keep Render App Alive
on:
  schedule:
    - cron: '*/10 * * * *'  # Every 10 minutes
jobs:
  keep-alive:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Render App
        run: curl -f "${{ secrets.RENDER_APP_URL }}/health/"
```

#### Option C: Local Script (FREE)
Run the included `keep_alive.py`:
```bash
pip install requests
python keep_alive.py
```

## 🔧 Environment Variables

Add these to your Render service:

```
SECRET_KEY=django-insecure-your-secret-key-here-make-it-long-and-random
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
BASE_URL=https://your-app-name.onrender.com
```

## 📊 Health Endpoints

Your app has these endpoints for monitoring:

- **Health Check**: `https://your-app-name.onrender.com/health/`
- **Keep-Alive**: `https://your-app-name.onrender.com/keep-alive/`
- **Recovery**: `https://your-app-name.onrender.com/recovery/`

## 🎯 Expected Results

After setup:
- ✅ **App deployed** at `https://your-app-name.onrender.com`
- ✅ **No sleep mode** (with keep-alive)
- ✅ **PostgreSQL database** working
- ✅ **Health monitoring** active
- ✅ **Admin access** at `/admin/`

## 🆘 Troubleshooting

### App Goes to Sleep
1. **Check keep-alive service** is running
2. **Verify health endpoint** responds
3. **Try different keep-alive solution**
4. **Check Render logs** for errors

### Database Issues
1. **Verify DATABASE_URL** is correct
2. **Check PostgreSQL service** is running
3. **Run migrations**: `python manage.py migrate`

### Build Failures
1. **Check requirements.txt** exists
2. **Verify build.sh** has execute permissions
3. **Check build logs** for specific errors

## 💡 Pro Tips

- **Use UptimeRobot** for reliable monitoring
- **Monitor Render dashboard** regularly
- **Set up multiple keep-alive methods** for redundancy
- **Check app logs** if issues occur

## 🎉 Success!

Your TeamTrack app will be:
- **Always online** (no sleep mode)
- **Fully functional** with all features
- **Monitored** for uptime
- **Ready for your team** to use!

---

**Need help?** Check the logs in Render dashboard or try a different keep-alive solution.
