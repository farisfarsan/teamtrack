@echo off
echo Starting TeamTrack Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Installing dependencies...
pip install -r requirements.txt

REM Run deployment script
echo Running deployment...
python deploy.py

REM Start the server
echo.
echo Starting server on all network interfaces...
echo Team members can access at: http://YOUR_IP_ADDRESS:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver 0.0.0.0:8000

pause
