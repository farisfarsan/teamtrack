# Render Keep-Alive Service Configuration

## 🚀 Multiple Keep-Alive Solutions for Render.com

### Solution 1: External Monitoring Service (Recommended)

Use **UptimeRobot** (Free):
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Sign up for free account
3. Add new monitor:
   - **Monitor Type**: HTTP(s)
   - **URL**: `https://your-app-name.onrender.com/health/`
   - **Monitoring Interval**: 5 minutes
   - **Monitor Timeout**: 30 seconds

### Solution 2: GitHub Actions (Free)

Create `.github/workflows/keep-alive.yml`:

```yaml
name: Keep Render App Alive
on:
  schedule:
    - cron: '*/10 * * * *'  # Every 10 minutes
  workflow_dispatch:

jobs:
  keep-alive:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Render App
        run: |
          curl -f "${{ secrets.RENDER_APP_URL }}/health/" || echo "Ping failed"
```

### Solution 3: Local Keep-Alive Script

Run the included `keep_alive.py` script on your computer:

```bash
# Install requirements
pip install requests

# Run the script (update URL first)
python keep_alive.py
```

### Solution 4: Cron Job (Linux/Mac)

Add to your crontab:

```bash
# Edit crontab
crontab -e

# Add this line (runs every 10 minutes)
*/10 * * * * curl -f https://your-app-name.onrender.com/health/ > /dev/null 2>&1
```

### Solution 5: Online Cron Services (Free)

Use **cron-job.org**:
1. Go to [cron-job.org](https://cron-job.org)
2. Create free account
3. Add new cron job:
   - **URL**: `https://your-app-name.onrender.com/health/`
   - **Schedule**: Every 10 minutes
   - **Method**: GET

## 🔧 Setup Instructions

1. **Deploy to Render** using your existing guide
2. **Choose one keep-alive solution** from above
3. **Update the URL** in the chosen solution
4. **Test the solution** to ensure it works

## 📊 Monitoring

Check if your app stays alive:
- Monitor Render dashboard
- Check app logs
- Test app responsiveness

## 💡 Pro Tips

- **UptimeRobot** is the most reliable free option
- **GitHub Actions** works well if you use GitHub
- **Multiple solutions** can be used together for redundancy
- **Monitor your app** to ensure keep-alive is working

## 🆘 Troubleshooting

If your app still goes to sleep:
1. Check if the health endpoint exists
2. Verify the URL is correct
3. Try a different keep-alive solution
4. Consider upgrading to Render's paid plan
