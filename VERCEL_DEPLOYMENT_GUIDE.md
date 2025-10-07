# 🚀 Vercel Deployment Guide for TeamTrack

## 🌟 Why Vercel?

- ✅ **Completely free** for personal projects
- ✅ **Automatic deployments** from GitHub
- ✅ **Built-in PostgreSQL** database
- ✅ **Custom domain** support
- ✅ **Global CDN** for fast loading
- ✅ **No credit card** required
- ✅ **Easy setup** with great documentation

---

## 📋 Step-by-Step Deployment

### Step 1: Prepare Your Code

#### Run the Vercel deployment helper:
```bash
python deploy_vercel.py
```

This will:
- Initialize git repository
- Create .gitignore file
- Commit all files
- Prepare for deployment

### Step 2: Push to GitHub

#### Create GitHub Repository:
1. **Go to** https://github.com
2. **Sign up** or login
3. **Click "New repository"**
4. **Name it** "teamtrack"
5. **Make it public** (required for free Vercel)
6. **Click "Create repository"**

#### Push Your Code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/teamtrack.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Vercel

#### Create Vercel Account:
1. **Go to** https://vercel.com
2. **Sign up** with GitHub
3. **Connect your GitHub account**

#### Deploy Your Project:
1. **Click "New Project"**
2. **Import your teamtrack repository**
3. **Configure settings**:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)

#### Set Environment Variables:
1. **Go to Project Settings**
2. **Click "Environment Variables"**
3. **Add these variables**:
   ```
   SECRET_KEY = your-super-secret-key-here-change-this
   DEBUG = False
   ALLOWED_HOSTS = your-project-name.vercel.app
   ```

### Step 4: Add Database

#### Add Vercel Postgres:
1. **Go to your project dashboard**
2. **Click "Storage" tab**
3. **Click "Create Database"**
4. **Select "Postgres"**
5. **Name it** "teamtrack-db"
6. **Click "Create"**

#### Configure Database Environment Variables:
Vercel will automatically add these:
```
POSTGRES_DATABASE = your-db-name
POSTGRES_USER = your-db-user
POSTGRES_PASSWORD = your-db-password
POSTGRES_HOST = your-db-host
POSTGRES_PORT = 5432
```

### Step 5: Run Migrations

#### Using Vercel CLI (Recommended):
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Link to your project
vercel link

# Run migrations
vercel env pull .env.local
python manage.py migrate
```

#### Or using Vercel Dashboard:
1. **Go to your project**
2. **Click "Functions" tab**
3. **Create a new function** to run migrations
4. **Or use the Vercel CLI method above**

### Step 6: Deploy!

#### Automatic Deployment:
- **Vercel will automatically deploy** when you push to GitHub
- **Your app will be available** at `https://your-project-name.vercel.app`

#### Manual Deployment:
```bash
vercel --prod
```

---

## 🔧 Configuration Details

### Environment Variables Required:

```env
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=your-project-name.vercel.app
POSTGRES_DATABASE=your-db-name
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password
POSTGRES_HOST=your-db-host
POSTGRES_PORT=5432
```

### Vercel Configuration (vercel.json):
```json
{
  "version": 2,
  "builds": [
    {
      "src": "manage.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "manage.py"
    }
  ]
}
```

---

## 👥 Team Access

### After Deployment:
Your team can access TeamTrack at:
```
https://your-project-name.vercel.app
```

### Login Credentials (Same as Before):
- **Faris**: farismullen93@gmail.com / farisgryttuser1
- **Dileep**: dileepkrishnan92@gmail.com / dileep123
- **Vyshak**: vyshakpk10@gmail.com / vyshak123
- **Febi**: febiwilsonvazhakkan@gmail.com / febi123
- **Syam**: muralisyam1@gmail.com / murali123

---

## 🎯 Quick Start Commands

### Complete Deployment:
```bash
# 1. Prepare code
python deploy_vercel.py

# 2. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/teamtrack.git
git push -u origin main

# 3. Deploy on Vercel
# - Go to vercel.com
# - Import GitHub repository
# - Add environment variables
# - Add PostgreSQL database
# - Deploy!

# 4. Run migrations (using Vercel CLI)
npm i -g vercel
vercel login
vercel link
vercel env pull .env.local
python manage.py migrate
```

---

## 🔒 Security & Production

### Security Settings:
- ✅ **HTTPS enabled** automatically
- ✅ **Secure cookies** configured
- ✅ **XSS protection** enabled
- ✅ **CSRF protection** enabled
- ✅ **Environment variables** secured

### Production Checklist:
- ✅ **Change SECRET_KEY** to a random string
- ✅ **Set DEBUG=False**
- ✅ **Configure ALLOWED_HOSTS**
- ✅ **Use strong passwords**
- ✅ **Enable database backups**

---

## 🆘 Troubleshooting

### Common Issues:

#### Build Errors:
```bash
# Check build logs in Vercel dashboard
# Ensure all dependencies are in requirements.txt
```

#### Database Connection:
```bash
# Verify environment variables are set
# Check database is created and running
```

#### Static Files:
```bash
# Vercel handles static files automatically
# No additional configuration needed
```

#### Migration Issues:
```bash
# Run migrations using Vercel CLI
vercel env pull .env.local
python manage.py migrate
```

---

## 🎉 Benefits of Vercel

### Performance:
- ✅ **Global CDN** - Fast loading worldwide
- ✅ **Automatic scaling** - Handles traffic spikes
- ✅ **Edge functions** - Serverless architecture
- ✅ **Instant deployments** - Push to deploy

### Developer Experience:
- ✅ **GitHub integration** - Automatic deployments
- ✅ **Preview deployments** - Test before production
- ✅ **Analytics** - Built-in performance monitoring
- ✅ **Custom domains** - Professional URLs

### Team Collaboration:
- ✅ **Global access** - Team members worldwide
- ✅ **Always online** - No server management
- ✅ **Automatic backups** - Data protection
- ✅ **Professional URLs** - Brand credibility

---

## 🚀 Success!

Once deployed, your TeamTrack application will be:
- **Accessible globally** at your Vercel URL
- **Always online** with automatic scaling
- **Fast loading** with global CDN
- **Professional** with custom domain support
- **Secure** with HTTPS and modern security features

Your team can now access TeamTrack from anywhere in the world! 🌍
