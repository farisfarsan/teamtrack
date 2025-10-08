# TeamTrack Deployment Guide for Render

## 🚀 Deploy TeamTrack to Render

This guide will help you deploy your TeamTrack application to Render.com.

### 📋 Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Environment Variables**: Prepare your production settings

### 🔧 Step 1: Prepare Your Repository

Make sure your repository has these files:
- `requirements_render.txt` - Production dependencies
- `build.sh` - Build script for Render
- `teamtrack/settings_render.py` - Production settings
- `.env.example` - Environment variables template

### 🌐 Step 2: Create Web Service on Render

1. **Go to Render Dashboard**
   - Visit [render.com/dashboard](https://render.com/dashboard)
   - Click "New +" → "Web Service"

2. **Connect Repository**
   - Connect your GitHub account
   - Select your TeamTrack repository
   - Choose the branch (usually `main` or `master`)

3. **Configure Service Settings**
   ```
   Name: teamtrack
   Runtime: Python 3
   Build Command: ./build.sh
   Start Command: gunicorn teamtrack.wsgi:application --settings=teamtrack.settings_render
   ```

### 🗄️ Step 3: Add PostgreSQL Database

1. **Create Database**
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - Name: `teamtrack-db`
   - Choose plan (Free tier available)

2. **Get Database URL**
   - Copy the "External Database URL"
   - You'll use this in environment variables

### ⚙️ Step 4: Configure Environment Variables

In your Render web service settings, add these environment variables:

```
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
```

**Important**: 
- Generate a strong SECRET_KEY (use Django's `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- Set DEBUG=False for production
- DATABASE_URL will be provided by Render's PostgreSQL service

### 🚀 Step 5: Deploy

1. **Save Settings**: Click "Save" in your web service configuration
2. **Deploy**: Render will automatically start building and deploying
3. **Monitor**: Watch the build logs for any errors

### 🔍 Step 6: Verify Deployment

1. **Check URL**: Your app will be available at `https://your-app-name.onrender.com`
2. **Test Login**: Use the admin credentials:
   - Email: `admin@example.com`
   - Password: `admin123`

### 👥 Step 7: Create Team Members

After deployment, create your team members using the management command:

```bash
# Access Render shell (if available) or use Django admin
python manage.py create_users
```

### 🔧 Step 8: Configure Custom Domain (Optional)

1. **Add Custom Domain**
   - Go to your service settings
   - Add your custom domain
   - Update DNS records as instructed

2. **Update ALLOWED_HOSTS**
   - Add your domain to `ALLOWED_HOSTS` in `settings_render.py`

### 📊 Step 9: Monitor and Maintain

1. **Logs**: Monitor application logs in Render dashboard
2. **Metrics**: Check performance metrics
3. **Updates**: Deploy updates by pushing to your repository

### 🆘 Troubleshooting

**Common Issues:**

1. **Build Fails**
   - Check `requirements_render.txt` for correct dependencies
   - Verify `build.sh` has execute permissions
   - Check build logs for specific errors

2. **Database Connection Issues**
   - Verify DATABASE_URL is correct
   - Check PostgreSQL service is running
   - Ensure database exists

3. **Static Files Not Loading**
   - Verify `collectstatic` runs in build script
   - Check WhiteNoise configuration
   - Ensure STATIC_ROOT is set correctly

4. **Environment Variables**
   - Double-check all required variables are set
   - Verify SECRET_KEY is strong and unique
   - Ensure DEBUG=False for production

### 🔐 Security Checklist

- [ ] Strong SECRET_KEY generated
- [ ] DEBUG=False in production
- [ ] HTTPS enabled (Render provides this)
- [ ] Database credentials secured
- [ ] Static files properly configured
- [ ] CSRF_TRUSTED_ORIGINS updated

### 📈 Performance Tips

1. **Database Indexing**: Add indexes for frequently queried fields
2. **Caching**: Consider Redis for caching (Render provides this)
3. **CDN**: Use Render's CDN for static files
4. **Monitoring**: Set up uptime monitoring

### 🎉 Success!

Your TeamTrack application should now be live and accessible to your team members!

**Default Admin Credentials:**
- Email: `admin@example.com`
- Password: `admin123`

**Team Member Credentials:**
- See the user credentials table from earlier in the conversation

---

## 📞 Support

If you encounter issues:
1. Check Render's documentation
2. Review Django deployment best practices
3. Check application logs in Render dashboard
4. Verify all environment variables are set correctly
