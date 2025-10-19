# 🔒 Data Safety Guide for Render

## ✅ **Your Data is SAFE!**

### **What Persists:**
- ✅ **User accounts** - All user data saved in PostgreSQL
- ✅ **Tasks** - All task data saved in database
- ✅ **Attendance records** - All attendance data saved
- ✅ **Settings** - All app settings saved
- ✅ **Relationships** - User-team relationships saved

### **What Gets Cleared:**
- ❌ **File uploads** (if stored locally)
- ❌ **Temporary session data**
- ❌ **Cache data**

## 🗄️ **Database Persistence**

**PostgreSQL Database:**
- **Always online** - Even when your app sleeps
- **Survives deployments** - Data stays through updates
- **Survives restarts** - App reconnects to same database
- **Only deleted manually** - You control when it's deleted

## 🔄 **What Happens During Sleep Mode:**

1. **App goes to sleep** (free tier after 15 minutes)
2. **Database stays online** 24/7
3. **User visits app** → App wakes up
4. **App reconnects** to same database
5. **All data is still there!**

## 💾 **Backup Options:**

### **Option 1: Manual Backup (Free)**
```bash
# Run this command in Render shell
python manage.py backup_db
```

### **Option 2: Automated Backup (Paid)**
- **Render Cron Jobs** - Run backups daily
- **External services** - Automated database backups

### **Option 3: Export Data (Free)**
```bash
# Export specific data
python manage.py dumpdata accounts > users.json
python manage.py dumpdata tasks > tasks.json
```

## 🛡️ **Data Safety Tips:**

1. **Never delete** the PostgreSQL service
2. **Use database backups** for important data
3. **Test restores** to ensure backups work
4. **Monitor database** usage and limits

## 📊 **Data Storage Summary:**

| Data Type | Storage | Persistence |
|-----------|---------|-------------|
| User Accounts | PostgreSQL | ✅ Permanent |
| Tasks | PostgreSQL | ✅ Permanent |
| Attendance | PostgreSQL | ✅ Permanent |
| Settings | PostgreSQL | ✅ Permanent |
| File Uploads | Local Disk | ❌ Temporary |
| Sessions | Memory | ❌ Temporary |

## 🎯 **Bottom Line:**

**Your core data (users, tasks, attendance) is SAFE and will NOT be cleared when Render goes down!**

The only data that gets cleared is temporary data like sessions and local file uploads.
