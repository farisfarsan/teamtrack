#!/bin/bash
# Quick Fix Script for Render 503 Error

echo "🔧 Render 503 Error - Quick Fix Guide"
echo "======================================"

echo ""
echo "1. Check Render Dashboard:"
echo "   - Go to render.com/dashboard"
echo "   - Click on your service"
echo "   - Check 'Logs' tab for errors"

echo ""
echo "2. Verify Environment Variables:"
echo "   SECRET_KEY=django-insecure-your-secret-key-here"
echo "   DEBUG=False"
echo "   DATABASE_URL=postgresql://user:pass@host:port/db"

echo ""
echo "3. Check Build Command:"
echo "   ./build.sh"

echo ""
echo "4. Check Start Command:"
echo "   gunicorn teamtrack.wsgi:application --settings=teamtrack.settings_render"

echo ""
echo "5. Common Issues:"
echo "   - Missing requirements.txt"
echo "   - Wrong Python version"
echo "   - Database connection issues"
echo "   - Missing environment variables"

echo ""
echo "6. Quick Test:"
echo "   - Try accessing: https://teamtrack1.onrender.com/health/"
echo "   - Check if health endpoint responds"

echo ""
echo "✅ If still having issues, check Render logs for specific error messages!"
